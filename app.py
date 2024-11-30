from flask import Flask, render_template, redirect, request, url_for, send_from_directory
import random
from datetime import datetime
import os

app = Flask(__name__, template_folder="templates")

# routess
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/status")
def status():
    date = datetime.now().strftime("%B, %d, %Y")
    return render_template("status.html", date=date)
    
@app.route('/login_files/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'login_files'), filename)

if __name__ == "__main__":
    app.run(debug=True)
    