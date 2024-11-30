from flask import Flask, render_template, redirect, request, url_for, send_from_directory
import random
from datetime import datetime
import os

app = Flask(__name__, template_folder="templates")

user_data = {"name": "", "date": ""}

# List of universities
university_list = [
    {"name": "University of Chicago", "logo": "static/logos/uchicago-logo.jpg"},
    {"name": "Harvard University", "logo": "static/logos/harvard-logo.jpg"},
]

# Intro Page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_data["name"] = request.form["name"]
        user_data["date"] = datetime.strptime(request.form["date"], "%Y-%m-%d").strftime("%B %d, %Y")
        return redirect(url_for("select_university"))
    return render_template("index.html")

# University Selection Page
@app.route("/universities", methods=["GET", "POST"])
def select_university():
    return render_template("universities.html", name=user_data["name"], university_list=university_list)

# Status Simulation Page
@app.route("/ustatus/<college>", methods=["GET", "POST"])
def ustatus(college):
    if request.method == "POST":
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college))
        return redirect(url_for("rejection", college=college))
    return render_template("ustatus.html", name=user_data["name"], date=user_data["date"], college=college)

# Acceptance Page
@app.route("/acceptance/<college>")
def acceptance(college):
    return render_template("acceptance.html", name=user_data["name"], date=user_data["date"], college=college)

# Rejection Page
@app.route("/rejection/<college>")
def rejection(college):
    return render_template("rejection.html", name=user_data["name"], date=user_data["date"], college=college)

# files routes    
@app.route('/login_files/<path:filename>')
def login_files_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'login_files'), filename)

@app.route('/ustatus_files/<path:filename>')
def ustatus_files_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'ustatus_files'), filename)

@app.route('/acceptance_files/<path:filename>')
def acceptance_files_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'acceptance_files'), filename)

@app.route('/ball_images/<path:filename>')
def ball_files_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'ball_images'), filename)

@app.route('/rejection_files/<path:filename>')
def rejection_files_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'rejection_files'), filename)


if __name__ == "__main__":
    app.run(debug=True)
    