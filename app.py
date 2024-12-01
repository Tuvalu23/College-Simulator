from flask import Flask, render_template, redirect, request, url_for, send_from_directory
import random
from datetime import datetime
import os

app = Flask(__name__, template_folder="templates")

user_data = {"name": "", "date": ""}

# List of universities
university_list = [
    {"name": "cornell", "display_name": "Cornell University", "logo": "static/logos/cornell-logo.jpg"},
    {"name": "harvard", "display_name": "Harvard University", "logo": "static/logos/harvard-logo.jpg"},
    {"name": "mit", "display_name": "Massachusetts Institute of Technology", "logo": "static/logos/mit-logo.jpg"},
    {"name": "princeton", "display_name": "Princeton University", "logo": "static/logos/princeton-logo.jpg"},
    {"name": "stanford", "display_name": "Stanford University", "logo": "static/logos/stanford-logo.jpg"},
    {"name": "uchicago", "display_name": "University of Chicago", "logo": "static/logos/uchicago-logo.jpg"},
    {"name": "yale", "display_name": "Yale University", "logo": "static/logos/yale-logo.jpg"},
    
]


# Intro Page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_data["name"] = request.form["name"]
        user_data["date"] = datetime.strptime(request.form["date"], "%Y-%m-%d").strftime("%B %d, %Y")
        return redirect(url_for("select_university"))
    return render_template("index.html", user_data=user_data)

# University Selection Page
@app.route("/universities", methods=["GET", "POST"])
def select_university():
    return render_template("universities.html", name=user_data["name"], university_list=university_list, user_data=user_data)

@app.route("/<college>/login", methods=["GET", "POST"])
def login(college):
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Check for missing inputs
        if not email or not password:
            return render_template(f"{college}/login.html", error="Please fill out all fields.", college=college)
        
        # Redirect to ustatus if inputs are valid
        return redirect(url_for("ustatus", college=college))
    
    return render_template(f"{college}/login.html", name=user_data["name"], college=college)

@app.route("/<college>/ustatus", methods=["GET", "POST"])
def ustatus(college):
    if college == "mit":
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college, name=user_data["name"]))
        return redirect(url_for("rejection", college=college, name=user_data["name"]))
    
    if request.method == "POST":
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college))
        return redirect(url_for("rejection", college=college))
    return render_template(f"{college}/ustatus.html", name=user_data["name"], date=user_data["date"], college=college)

# Acceptance Page
@app.route("/<college>/acceptance")
def acceptance(college):
    return render_template(f"{college}/acceptance.html", name=user_data["name"], date=user_data["date"], college=college)

# Rejection Page
@app.route("/<college>/rejection")
def rejection(college):
    return render_template(f"{college}/rejection.html", name=user_data["name"], date=user_data["date"], college=college)

# files
@app.route('/<college>/login_files/<path:filename>')
def login_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'login_files'), filename)

@app.route('/<college>/ustatus_files/<path:filename>')
def ustatus_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'ustatus_files'), filename)

@app.route('/<college>/acceptance_files/<path:filename>')
def acceptance_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'acceptance_files'), filename)

@app.route('/<college>/ball_images/<path:filename>')
def ball_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'ball_images'), filename)

@app.route('/<college>/rejection_files/<path:filename>')
def rejection_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'rejection_files'), filename)



if __name__ == "__main__":
    app.run(debug=True)
    