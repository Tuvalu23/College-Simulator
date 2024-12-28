import random
from datetime import datetime, timedelta
import os

from flask import Flask, render_template, redirect, request, url_for, send_from_directory, session, flash
from functools import wraps
from models import init_db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="templates")
app.secret_key = 'Tuvalu23'

# init db
init_db()

# List of universities
university_list = [
    {
        "name": "bing",
        "display_name": "Binghamton University",
        "logo": "static/logos/bing-logo.png",
        "description": "Binghamton University, located in Vestal, NY, is a top public institution known for its strong research programs, affordability, and vibrant campus life. It offers a diverse range of undergraduate and graduate programs that prepare students for successful careers and leadership roles.",
        "badges": [
            {"label": "Public", "color": "Public"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Research", "color": "Research"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Affordable", "color": "Affordable"},
            {"label": "Diverse", "color": "Diverse"}
        ]
    },
    {
        "name": "brown",
        "display_name": "Brown University",
        "logo": "static/logos/brown-logo.jpg",
        "description": "Brown University in Providence, RI, is an esteemed Ivy League institution celebrated for its Open Curriculum, fostering academic freedom and interdisciplinary studies. It boasts a vibrant community committed to research, creativity, and global engagement.",
        "badges": [
            {"label": "T-10", "color": "T-10"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Research", "color": "Research"},
            {"label": "Innovative", "color": "Innovative"},
            {"label": "Creative", "color": "Creative"}
        ]
    },
    {
        "name": "buffalo",
        "display_name": "University at Buffalo",
        "logo": "static/logos/buffalo-logo.jpg",
        "description": "The University at Buffalo, part of the SUNY system, is a large public research university in Buffalo, NY. It is recognized for its robust academic programs, cutting-edge research initiatives, and commitment to community engagement.",
        "badges": [
            {"label": "Public", "color": "Public"},
            {"label": "Urban", "color": "Urban"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Diverse", "color": "Diverse"},
            {"label": "Research", "color": "Research"},
            {"label": "Innovation", "color": "Innovation"}
        ]
    },
    {
        "name": "caltech",
        "display_name": "California Institute of Technology",
        "logo": "static/logos/caltech-logo.jpg",
        "description": "Caltech in Pasadena, CA, is a world-renowned private institution specializing in science and engineering. It fosters a collaborative environment that encourages innovation and scientific discovery with a highly selective student body.",
        "badges": [
            {"label": "T-5", "color": "T-5"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Innovative", "color": "Innovative"},
            {"label": "Research", "color": "Research"},
            {"label": "Engineering", "color": "Engineering"}
        ]
    },
    {
        "name": "cmu",
        "display_name": "Carnegie Mellon University",
        "logo": "static/logos/cmu-logo.jpg",
        "description": "Carnegie Mellon University in Pittsburgh, PA, is a leading global research institution known for its exceptional programs in computer science, engineering, and the arts. It promotes interdisciplinary research and creative innovation within a collaborative academic environment.",
        "badges": [
            {"label": "T-20", "color": "T-20"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Innovative", "color": "Innovative"},
            {"label": "Computer Science", "color": "Computer Science"},
            {"label": "Arts", "color": "Arts"}
        ]
    },
    {
        "name": "columbia",
        "display_name": "Columbia University",
        "logo": "static/logos/columbia-logo.jpg",
        "description": "Columbia University in New York City is an esteemed Ivy League institution known for its rigorous Core Curriculum and commitment to academic excellence. Located in the heart of NYC, it offers a dynamic environment that blends tradition with innovation.",
        "badges": [
            {"label": "T-5", "color": "T-5"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Research", "color": "Research"},
            {"label": "Diverse", "color": "Diverse"},
            {"label": "Global", "color": "Global"},
            {"label": "Liberal Arts", "color": "Liberal Arts"}
        ]
    },
    {
        "name": "cornell",
        "display_name": "Cornell University",
        "logo": "static/logos/cornell-logo.jpg",
        "description": "Cornell University in Ithaca, NY, is a distinguished Ivy League and land-grant institution known for its comprehensive academic programs and strong research initiatives. It fosters innovation and excellence across multiple disciplines.",
        "badges": [
            {"label": "T-10", "color": "T-10"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Rural", "color": "Rural"},
            {"label": "Research", "color": "Research"},
            {"label": "Engineering", "color": "Engineering"},
            {"label": "Land-Grant", "color": "Land-Grant"},
            {"label": "Agriculture", "color": "Agriculture"}
        ]
    },
    {
        "name": "dartmouth",
        "display_name": "Dartmouth College",
        "logo": "static/logos/dartmouth-logo.png",
        "description": "Dartmouth College in Hanover, NH, is a prestigious Ivy League institution focusing on liberal arts education and undergraduate teaching. It offers a close-knit community that encourages academic rigor and personal growth.",
        "badges": [
            {"label": "T-10", "color": "T-10"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Rural", "color": "Rural"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Undergraduate", "color": "Undergraduate"},
            {"label": "Research", "color": "Research"},
            {"label": "Tradition", "color": "Tradition"}
        ]
    },
    {
        "name": "duke",
        "display_name": "Duke University",
        "logo": "static/logos/duke-logo.jpg",
        "description": "Duke University in Durham, NC, is a prestigious private research institution renowned for its strong programs in research, health sciences, and athletics. It blends academic excellence with a vibrant campus life.",
        "badges": [
            {"label": "T-10", "color": "T-10"},
            {"label": "Private", "color": "Private"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Research", "color": "Research"},
            {"label": "Health Sciences", "color": "Health Sciences"},
            {"label": "Athletics", "color": "Athletics"},
            {"label": "Leadership", "color": "Leadership"}
        ]
    },
    {
        "name": "emory",
        "display_name": "Emory University",
        "logo": "static/logos/emory-logo.jpg",
        "description": "Emory University in Atlanta, GA, is a distinguished private institution known for its strong programs in liberal arts and health sciences. It offers a collaborative environment that fosters academic excellence and community engagement.",
        "badges": [
            {"label": "T-30", "color": "T-30"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Research", "color": "Research"},
            {"label": "Health Sciences", "color": "Health Sciences"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Community", "color": "Community"}
        ]
    },
    {
    "name": "georgetown",
    "display_name": "Georgetown University",
    "logo": "static/logos/georgetown-logo.jpg",
    "description": "Georgetown University, located in Washington, D.C., is a prestigious private institution renowned for its strong liberal arts and professional programs, historic campus, and commitment to fostering global leaders.",
    "badges": [
        {"label": "T-30", "color": "T-30"},
        {"label": "Private", "color": "Private"},
        {"label": "Urban", "color": "Urban"},
        {"label": "Research", "color": "Research"},
        {"label": "Liberal Arts", "color": "Liberal Arts"},
        {"label": "Prestigious", "color": "Prestigious"},
        {"label": "Global", "color": "Global"},
        {"label": "Law", "color": "Law"}
    ]
},
    {
        "name": "gtech",
        "display_name": "Georgia Tech",
        "logo": "static/logos/gtech-logo.jpg",
        "description": "Georgia Institute of Technology in Atlanta, GA, is a premier public research university renowned for its exceptional engineering and technology programs. It fosters innovation and excellence through cutting-edge research and collaborative initiatives.",
        "badges": [
            {"label": "T-30", "color": "T-30"},
            {"label": "Public", "color": "Public"},
            {"label": "Urban", "color": "Urban"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Innovative", "color": "Innovative"},
            {"label": "Engineering", "color": "Engineering"},
            {"label": "Technology", "color": "Technology"}
        ]
    },
    {
        "name": "harvard",
        "display_name": "Harvard University",
        "logo": "static/logos/harvard-logo.jpg",
        "description": "Harvard University in Cambridge, MA, is the oldest higher education institution in the U.S., consistently ranked among the world's top universities. It is renowned for its extensive research programs, diverse academic offerings, and influential alumni network.",
        "badges": [
            {"label": "T-5", "color": "T-5"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Research", "color": "Research"},
            {"label": "Global", "color": "Global"},
            {"label": "Leadership", "color": "Leadership"}
        ]
    },
    {
        "name": "jhu",
        "display_name": "Johns Hopkins University",
        "logo": "static/logos/jhu-logo.jpg",
        "description": "Johns Hopkins University in Baltimore, MD, is a world-leading research institution renowned for its contributions to medicine, public health, and scientific disciplines. It offers a collaborative academic environment with state-of-the-art facilities.",
        "badges": [
            {"label": "T-20", "color": "T-20"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Research", "color": "Research"},
            {"label": "Health Sciences", "color": "Health Sciences"},
            {"label": "Medicine", "color": "Medicine"},
            {"label": "Public Health", "color": "Public Health"}
        ]
    },
    {
        "name": "mit",
        "display_name": "Massachusetts Institute of Technology",
        "logo": "static/logos/mit-logo.jpg",
        "description": "MIT in Cambridge, MA, is a global leader in STEM education, research, and innovation. Known for its cutting-edge engineering and technology programs, MIT fosters a collaborative and entrepreneurial environment.",
        "badges": [
            {"label": "T-5", "color": "T-5"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Innovative", "color": "Innovative"},
            {"label": "Engineering", "color": "Engineering"},
            {"label": "Technology", "color": "Technology"}
        ]
    },
    {
    "name": "northeastern",
    "display_name": "Northeastern University",
    "logo": "static/logos/northeastern-logo.jpg",
    "description": "Northeastern University, located in Boston, MA, is renowned for its experiential learning model, including co-op programs that integrate classroom study with professional experience.",
    "badges": [
        {"label": "Private", "color": "Private"},
        {"label": "Urban", "color": "Urban"},
        {"label": "Research", "color": "Research"},
        {"label": "Global", "color": "Global"},
        {"label": "Co-op", "color": "Co-op"},
        {"label": "Innovation", "color": "Innovation"}
    ]
},
    {
        "name": "northwestern",
        "display_name": "Northwestern University",
        "logo": "static/logos/northwestern-logo.jpg",
        "description": "Northwestern University in Evanston, IL, near Chicago, is a premier private research institution known for its interdisciplinary studies and vibrant campus life.",
        "badges": [
            {"label": "T-10", "color": "T-10"},
            {"label": "Private", "color": "Private"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Research", "color": "Research"},
            {"label": "Performing Arts", "color": "Performing Arts"},
            {"label": "Innovation", "color": "Innovation"},
            {"label": "Media", "color": "Media"}
        ]
    },
    {
        "name": "nyu",
        "display_name": "New York University",
        "logo": "static/logos/nyu-logo.jpg",
        "description": "NYU in Manhattan, NY, is a leading private institution known for its global presence and diverse academic offerings. It provides unique opportunities for international study and excels in arts, business, law, and social sciences.",
        "badges": [
            {"label": "T-30", "color": "T-30"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Global", "color": "Global"},
            {"label": "Arts", "color": "Arts"},
            {"label": "International", "color": "International"}
        ]
    },
    {
        "name": "princeton",
        "display_name": "Princeton University",
        "logo": "static/logos/princeton-logo.jpg",
        "description": "Princeton University in Princeton, NJ, is a prestigious Ivy League institution known for its strong undergraduate focus and commitment to academic excellence. It offers diverse programs across the humanities, sciences, and engineering.",
        "badges": [
            {"label": "T-5", "color": "T-5"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Research", "color": "Research"},
            {"label": "Undergraduate", "color": "Undergraduate"},
            {"label": "Leadership", "color": "Leadership"}
        ]
    },
    {
        "name": "rice",
        "display_name": "Rice University",
        "logo": "static/logos/rice-logo.jpg",
        "description": "Rice University in Houston, TX, is a top private research institution known for its emphasis on STEM fields and a close-knit residential community. It offers comprehensive programs in engineering, sciences, humanities, and business.",
        "badges": [
            {"label": "T-15", "color": "T-15"}, 
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Residential", "color": "Residential"},
            {"label": "Research", "color": "Research"},
            {"label": "Business", "color": "Business"}
        ]
    },
    {
        "name": "stanford",
        "display_name": "Stanford University",
        "logo": "static/logos/stanford-logo.jpg",
        "description": "Stanford University near Silicon Valley, CA, is a leading private institution renowned for its entrepreneurial spirit and cutting-edge innovations. It offers diverse programs in engineering, business, humanities, and sciences.",
        "badges": [
            {"label": "T-5", "color": "T-5"},
            {"label": "Private", "color": "Private"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Research", "color": "Research"},
            {"label": "Entrepreneurial", "color": "Entrepreneurial"},
            {"label": "Innovation", "color": "Innovation"},
            {"label": "Leadership", "color": "Leadership"}
        ]
    },
    {
    "name": "tufts",
    "display_name": "Tufts University",
    "logo": "static/logos/tufts-logo.jpg",
    "description": "Tufts University, located in Medford and Somerville, MA, is a renowned institution recognized for its commitment to global leadership and civic engagement. It offers a vibrant mix of liberal arts, sciences, and professional schools within a collaborative and inclusive community.",
    "badges": [
        {"label": "T-30", "color": "T-30"},
        {"label": "Liberal Arts", "color": "Liberal Arts"},
        {"label": "Global", "color": "Global"},
        {"label": "Research", "color": "Research"},
        {"label": "Civic Engagement", "color": "Civic Engagement"},
        {"label": "Inclusive", "color": "Inclusive"}
    ]
},
    {
        "name": "berkeley",
        "display_name": "University of California, Berkeley",
        "logo": "static/logos/berkeley-logo.png",
        "description": "UC Berkeley in Berkeley, CA, is the flagship campus of the UC system and a top public university in the U.S. Renowned for its distinguished faculty and groundbreaking research, it offers a wide range of programs in arts, sciences, engineering, and business.",
        "badges": [
            {"label": "T-15", "color": "T-15"},
            {"label": "Public", "color": "Public"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Research", "color": "Research"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Innovation", "color": "Innovation"},
            {"label": "Diverse", "color": "Diverse"}
        ]
    },
    {
        "name": "umich",
        "display_name": "University of Michigan",
        "logo": "static/logos/umich-logo.png",
        "description": "The University of Michigan in Ann Arbor, MI, is a leading public research university known for its vibrant academic environment and outstanding athletic programs. It offers an array of programs across humanities, engineering, and business.",
        "badges": [
            {"label": "T-20", "color": "T-20"},
            {"label": "Public", "color": "Public"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Research", "color": "Research"},
            {"label": "Athletics", "color": "Athletics"},
            {"label": "STEM", "color": "STEM"},
            {"label": "Diverse", "color": "Diverse"}
        ]
    },
    {
        "name": "uchicago",
        "display_name": "University of Chicago",
        "logo": "static/logos/uchicago-logo.jpg",
        "description": "The University of Chicago in Chicago, IL, is renowned for its rigorous intellectual environment and influential Core Curriculum. As a prestigious private research university, it excels in economics, sociology, and various other disciplines.",
        "badges": [
            {"label": "T-10", "color": "T-10"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Economics", "color": "Economics"},
            {"label": "Research", "color": "Research"},
            {"label": "Intellectual", "color": "Intellectual"}
        ]
    },
    {
        "name": "upenn",
        "display_name": "University of Pennsylvania",
        "logo": "static/logos/upenn-logo.jpg",
        "description": "The University of Pennsylvania in Philadelphia, PA, is an esteemed Ivy League institution known for its prestigious Wharton School of Business and interdisciplinary education. It offers diverse programs in arts, sciences, engineering, and business within a dynamic urban setting.",
        "badges": [
            {"label": "T-10", "color": "T-10"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Research", "color": "Research"},
            {"label": "Business", "color": "Business"},
            {"label": "Wharton", "color": "Wharton"},
            {"label": "Leadership", "color": "Leadership"}
        ]
    },
    {
        "name": "usc",
        "display_name": "University of Southern California",
        "logo": "static/logos/usc-logo.png",
        "description": "USC in Los Angeles, CA, is a prestigious private research university known for its strong programs in film, business, and the arts. It offers a vibrant urban campus with ample opportunities for internships, networking, and creative expression.",
        "badges": [
            {"label": "T-30", "color": "T-30"},
            {"label": "Private", "color": "Private"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Film", "color": "Film"},
            {"label": "Business", "color": "Business"},
            {"label": "Innovation", "color": "Innovation"}
        ]
    },
    {
    "name": "uva",
    "display_name": "University of Virginia",
    "logo": "static/logos/uva-logo.jpg",
    "description": "The University of Virginia, located in Charlottesville, VA, is a prestigious public university known for its historic campus, academic excellence, and strong emphasis on student leadership and community engagement.",
    "badges": [
        {"label": "Public", "color": "Public"},
        {"label": "Suburban", "color": "Suburban"},
        {"label": "Historic", "color": "Historic"},
        {"label": "Leadership", "color": "Leadership"},
        {"label": "STEM", "color": "STEM"},
        {"label": "Community", "color": "Community"}
    ]
},
    {
        "name": "yale",
        "display_name": "Yale University",
        "logo": "static/logos/yale-logo.jpg",
        "description": "Yale University in New Haven, CT, is a prestigious Ivy League institution renowned for its outstanding programs in law, liberal arts, and the sciences. It offers a rich academic environment with a focus on research, intellectual growth, and leadership development.",
        "badges": [
            {"label": "T-5", "color": "T-5"},
            {"label": "Ivy", "color": "Ivy"},
            {"label": "Urban", "color": "Urban"},
            {"label": "Liberal Arts", "color": "Liberal Arts"},
            {"label": "Law", "color": "Law"},
            {"label": "Research", "color": "Research"},
            {"label": "Leadership", "color": "Leadership"}
        ]
    }
]

college_list = [
    ["columbia", "0.02", "1.9", "N", "P", "2024-12-18", "N", "2025-03-28"],
    ["stanford", "0.03", "N", "1.3", "REA", "2024-12-13", "N", "2025-03-29"],
    ["upenn", "0.03", "2", "N", "P", "2024-12-18", "N", "2025-03-28"],
    ["caltech", "0.03", "N", "1.1", "REA", "2024-12-12", "N", "2025-03-25"],
    ["jhu", "0.05", "1.7", "N", "P", "2024-12-13", "N", "2025-03-21"],
    ["dartmouth", "0.05", "2.3", "N", "P", "2024-12-13", "N", "2025-03-28"],
    ["princeton", "0.06", "N", "1.3", "REA", "2024-12-12", "N", "2025-03-28"],
    ["mit", "0.06", "N", "1.2", "P", "N", "2024-12-17", "2025-03-14"],
    ["yale", "0.07", "N", "1.3", "REA", "2024-12-17", "N", "2025-03-28"],
    ["harvard", "0.07", "N", "1.3", "REA", "2024-12-12", "N", "2025-03-28"],
    ["brown", "0.07", "2.0", "N", "P", "2024-12-13", "N", "2025-03-28"],
    ["uchicago", "0.09", "2.5", "1.1", "P", "2024-12-20", "2024-12-20", "2025-03-25"],
    ["northwestern", "0.09", "2.2", "N", "P", "2024-12-17", "N", "2025-03-24"],
    ["duke", "0.09", "2.0", "N", "P", "2024-12-16", "N", "2025-03-28"],
    ["cmu", "0.10", "1.2", "N", "P", "2024-12-13", "N", "2025-03-21"],
    ["rice", "0.12", "2", "N", "P", "2024-12-14", "N", "2025-03-21"],
    ["tufts", "0.14", "2.0", "N", "P", "2024-12-13", "N", "2025-3-22"],
    ["northeastern", "0.15", "2.7", "1.3", "P", "2024-12-11", "2025-1-31", "2025-3-17"],
    ["cornell", "0.15", "2.2", "N", "P", "2024-12-12", "N", "2025-03-28"],
    ["uva", "0.15", "2.3", "1.3", "PUB", "2024-12-13", "2025-2-15", "2025-3-21"],
    ["gtech", "0.15", "N", "1.4", "PUB", "N", "2025-1-27", "2025-03-22"],
    ["berkeley", "0.15", "N", "N", "PUB", "N", "N", "2025-03-27"],
    ["emory", "0.16", "1.7", "N", "P", "2024-12-11", "N", "2025-03-26"],
    ["usc", "0.17", "N", "1.3", "P", "N", "2025-1-17", "2025-03-16"],
    ["umich", "0.2", "N", "1.3", "PUB", "N", "2025-1-27", "2025-03-10"],
    ["nyu", "0.22", "1.5", "N", "P", "2024-12-12", "N", "2025-04-01"],
    ["georgetown", "0.23", "N", "1.3", "REA", "2024-12-13", "N", "2025-04-01"],
    ["bing", "0.65", "N", "1.3", "PUB", "N", "2024-11-20", "2025-02-15"],
    ["buffalo", "0.87", "N", "1.2", "PUB", "N", "2024-11-15", "2025-02-10"]
]

college_list_lower = [c[0].lower() for c in college_list]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to access this page.", "danger")
            return redirect(url_for('start'))
        return f(*args, **kwargs)
    return decorated_function

# login or register Page
@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.get_by_username(username)

        if user and User.verify_password(user['password_hash'], password):
            session['user_id'] = user['id']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('start'))

    return render_template('start.html')

# register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        errors = []
        # Basic server-side validation
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if len(password) < 5:
            errors.append("Password must be at least 5 characters long.")
            
        if User.get_by_username(username):
            errors.append("Username already exists.")

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('register'))

        User.create(username, password)
        flash("Account created successfully! Please login.", 'success')
        return redirect(url_for('start'))

    return render_template('register.html')

#dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    user = User.get_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)

# logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('start'))

# profile route (access user info etc)
@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        # Delete user account
        user = User.get_by_id(session['user_id'])
        if user:
            User.delete_user(user['id'])
            session.pop('user_id', None)
            flash("Your account has been deleted.", "info")
            return redirect(url_for('start'))
        else:
            flash("User not found.", "danger")
            return redirect(url_for('profile'))
    else:
        # GET request, show profile
        user_id = session['user_id']
        user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
        user = User.get_by_id(user_id)

        if user:
            username = user['username']
        else:
            username = "Unknown"

        # Fetch simulations to find the favorite and least favorite colleges
        simulations = User.get_simulations(user_id)
        college_counts = {}

        # Aggregate counts for each college
        for sim in simulations:
            college_counts[sim['university_name']] = college_counts.get(sim['university_name'], 0) + 1

        total_simulations = sum(college_counts.values())

        if college_counts:
            # Determine the most simulated (favorite) and least simulated (least favorite)
            favorite_college = max(college_counts, key=college_counts.get)
            least_favorite_college = min(college_counts, key=college_counts.get)

            # Fetch display names
            favorite_college_display = next(
                (uni['display_name'] for uni in university_list if uni['name'] == favorite_college), "Unknown"
            )
            least_favorite_college_display = next(
                (uni['display_name'] for uni in university_list if uni['name'] == least_favorite_college), "Unknown"
            )
        else:
            favorite_college_display = "No simulations yet"
            least_favorite_college_display = "No simulations yet"

        return render_template(
            "profile.html",
            name=user_data["name"],
            date=user_data["date"],
            username=username,
            favorite_college=favorite_college_display,
            least_favorite_college=least_favorite_college_display,
            total_simulations=total_simulations
        )
        
@app.route('/statistics')
@login_required
def statistics():
    user_id = session['user_id']
    simulations = User.get_simulations(user_id)  # Fetch user-specific simulations

    # Aggregate stats
    stats = {}
    for uni in university_list:
        uni_name = uni['name']
        uni_simulations = [sim for sim in simulations if sim['university_name'] == uni_name]
        total = len(uni_simulations)
        acceptances = len([sim for sim in uni_simulations if sim['result'] == 'acceptance']) \
                      + len([sim for sim in uni_simulations if sim['result'] == 'edacceptance'])
        rejections = len([sim for sim in uni_simulations if sim['result'] == 'rejection'])
        waitlists = len([sim for sim in uni_simulations if sim['result'] == 'waitlist'])
        deferrals = len([sim for sim in uni_simulations if sim['result'] == 'deferred'])

        success_rate = (acceptances / total * 100) if total > 0 else 0

        stats[uni_name] = {
            'display_name': uni['display_name'],
            'logo': uni['logo'],
            'description': uni['description'],
            'total_simulations': total,
            'acceptances': acceptances,
            'rejections': rejections,
            'waitlists': waitlists,
            'deferrals': deferrals,
            'success_rate': round(success_rate, 2),
            'badges': uni['badges']
        }

    # Sort stats for each leaderboard
    sorted_by_acceptances = sorted(stats.values(), key=lambda x: x['acceptances'], reverse=True)[:5]
    sorted_by_rejections = sorted(stats.values(), key=lambda x: x['rejections'], reverse=True)[:5]
    sorted_by_deferrals  = sorted(stats.values(), key=lambda x: x['deferrals'],  reverse=True)[:5]
    sorted_by_waitlists  = sorted(stats.values(), key=lambda x: x['waitlists'],  reverse=True)[:5]

    # Pass them all into the template
    return render_template(
        'statistics.html',
        acceptances_stats=sorted_by_acceptances,
        rejections_stats=sorted_by_rejections,
        deferrals_stats=sorted_by_deferrals,
        waitlists_stats=sorted_by_waitlists,
        # You also have sorted_stats for the Quick College Simulator
        sorted_stats=sorted(stats.values(), key=lambda x: x['total_simulations'], reverse=True),
    )
    
# quick sim
@app.route("/quicksim", methods=["GET", "POST"])
@login_required
def quicksim():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        date_input = request.form.get("date", "").strip()
        
        # Validate inputs
        if not name:
            flash("Name is required.", "danger")
            return redirect(url_for('quicksim'))
        if not date_input:
            flash("Date is required.", "danger")
            return redirect(url_for('quicksim'))
        
        # Process the date
        try:
            formatted_date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%B %d, %Y")
        except ValueError:
            flash("Invalid date format. Please select a valid date.", "danger")
            return redirect(url_for('quicksim'))
        
        # Store data in session
        session['quicksim_data'] = {
            "name": name,
            "date": formatted_date
        }
        
        flash("Quick Simulation data submitted successfully!", "success")
        return redirect(url_for("universities"))  # Ensure this route exists
    
    return render_template("quicksim.html")

# University Selection Page
@app.route("/quicksim/universities", methods=["GET", "POST"])
@login_required
def universities():
    # Retrieve user_data from session
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    
    # Ensure 'name' exists in user_data
    name = user_data.get("name", "User")
    date = user_data.get("date", "N/A")
    
    # Render the template with 'date' passed separately
    return render_template(
        "universities.html",
        name=name,
        date=date,
        university_list=university_list,
        user_data=user_data
    )

@app.route("/quicksim/<college>/login", methods=["GET", "POST"])
def login(college):
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Check for missing inputs
        if not email or not password:
            return render_template(f"{college}/login.html", error="Please fill out all fields.", college=college, date=user_data["date"])
        
        # Redirect to ustatus if inputs are valid
        return redirect(url_for("ustatus", college=college))
    
    return render_template(f"{college}/login.html", name=user_data["name"], college=college, date=user_data["date"])

# ustatus route
@app.route("/quicksim/<college>/ustatus", methods=["GET", "POST"])
def ustatus(college):
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    if request.method == "POST":
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college))
        return redirect(url_for("rejection", college=college))
    
   # Check if the college is Northeastern
    if college.lower() == "northeastern":
        # Simulate decision directly
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college))
        else:
            return redirect(url_for("rejection", college=college))
    else:
        # Redirect to ustatus for other colleges
        return redirect(url_for("ustatus", college=college))
    
    return render_template(f"{college}/login.html", name=user_data["name"], college=college, date=user_data["date"])

@app.route("/quicksim/<college>/acceptance")
def acceptance(college):
    user_id = session.get('user_id')
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    if user_id:
        User.log_simulation(user_id, college, 'acceptance')
    return render_template(f"{college}/acceptance.html", name=user_data["name"], date=user_data["date"], college=college)

@app.route("/quicksim/<college>/rejection")
def rejection(college):
    user_id = session.get('user_id')
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    if user_id:
        User.log_simulation(user_id, college, 'rejection')
    return render_template(f"{college}/rejection.html", name=user_data["name"], date=user_data["date"], college=college)

# advanced sm stuff
submissions = []

# Advanced Simulation Route
@app.route("/advancedsim", methods=["GET", "POST"])
@login_required
def advancedsim():
    clear_session()
    if request.method == "POST":
        # Extract form data
        name = request.form.get("name", "").strip()
        gpa = request.form.get("gpa", "").strip()
        test_option = request.form.get("test_option", "")
        sat_score = request.form.get("sat_score", "").strip()
        act_score = request.form.get("act_score", "").strip()
        extracurriculars = request.form.get("extracurriculars", "").strip()
        essays = request.form.get("essays", "").strip()
        ap_courses = request.form.get("ap_courses", "").strip()
        race_str = request.form.get("race", "").strip()
        gender_str = request.form.get("gender", "").strip()
        first_gen = request.form.get("first_gen", "off") == "on"

        # Mapping Dictionaries
        RACE_MAPPING = {
            "Caucasian": 1,
            "African-American": 2,
            "Hispanic or Latino": 3,
            "Asian": 4,
            "Native American or Alaskan Native": 5,
            "Pacific Islander": 6,
            "Middle Eastern or North African": 7,
            "Prefer not to say": 8,
            "Other": 9
        }

        GENDER_MAPPING = {
            "Male": 1,
            "Female": 2,
            "Other": 3  # Assuming 'Other' represents Non-binary or similar categories
        }

        # Initialize error flag and messages
        error = False
        error_messages = []

        # Server-side Validation
        if not name:
            error = True
            error_messages.append("Name is required.")

        try:
            gpa_val = float(gpa)
            if not (65 <= gpa_val <= 100):
                raise ValueError
        except ValueError:
            error = True
            error_messages.append("GPA must be a number between 65 and 100.")

        if test_option == 'sat':
            try:
                sat_val = int(sat_score)
                if not (400 <= sat_val <= 1600) or sat_val % 10 != 0:
                    raise ValueError
            except ValueError:
                error = True
                error_messages.append("SAT score must be an integer between 400 and 1600 in increments of 10.")
        elif test_option == 'act':
            try:
                act_val = int(act_score)
                if not (1 <= act_val <= 36):
                    raise ValueError
            except ValueError:
                error = True
                error_messages.append("ACT score must be an integer between 1 and 36.")

        try:
            extracurriculars_val = int(extracurriculars)
            if not (0 <= extracurriculars_val <= 10):
                raise ValueError
        except ValueError:
            error = True
            error_messages.append("Extracurricular activities rating must be an integer between 0 and 10.")

        try:
            essays_val = int(essays)
            if not (0 <= essays_val <= 10):
                raise ValueError
        except ValueError:
            error = True
            error_messages.append("Essays rating must be an integer between 0 and 10.")

        try:
            ap_val = int(ap_courses)
            if ap_val < 0:
                raise ValueError
        except ValueError:
            error = True
            error_messages.append("AP courses taken must be a non-negative integer.")

        if not race_str:
            error = True
            error_messages.append("Race/Ethnicity selection is required.")

        if not gender_str:
            error = True
            error_messages.append("Gender selection is required.")

        if error:
            for message in error_messages:
                flash(message, "danger")
            # Optionally, you can repopulate the form with previously entered data here
            return render_template("advancedsim.html")
        
        # Map race and gender strings to integer codes
        race = RACE_MAPPING.get(race_str)
        gender = GENDER_MAPPING.get(gender_str)

        # Validate mapping
        if race is None:
            flash("Invalid Race/Ethnicity selection.", "danger")
            return render_template("advancedsim.html")

        if gender is None:
            flash("Invalid Gender selection.", "danger")
            return render_template("advancedsim.html")

        # Function to compute demographic score
        def demScore(gender, race, firstGen):
            score = 5  # Base score

            # Gender-based adjustments
            if gender in [2, 3]:  # Female or Non-binary
                score += 2.3  # Fixed adjustment instead of random

            # First-generation adjustment
            if firstGen:
                score += 3  # Fixed adjustment instead of random

            # Race-based adjustments
            if race == 1:  # Caucasian
                score -= 2
            elif race == 2:  # African-American
                score += 4.5
            elif race == 3:  # Hispanic or Latino
                score += 4.5
            elif race == 4:  # Asian
                score -= 3.5
            elif race == 5:  # Native American or Alaskan Native
                score += 4
            elif race == 6:  # Pacific Islander
                score += 3
            elif race == 7:  # Middle Eastern or North African
                score += 2
            elif race == 8:  # Prefer not to say
                score -= 1
            elif race == 9:  # Other
                score += 1.5
            # No adjustment for undefined races

            score += random.uniform(-2, 2)
            # Clamp the score between 0 and 10
            score = max(0.0, min(score, 10.0))
            return round(score, 2)

        # Function to categorize the demographic score
        def rate(score):
            if 8.7 <= score <= 10:
                return "Outstanding", "outstanding"
            elif 7.2 <= score < 8.7:
                return "Strong", "strong"
            elif 6 <= score < 7.2:
                return "Moderate", "moderate"
            elif 4.5 <= score < 6:
                return "Fair", "fair"
            elif 2 <= score < 4.5:
                return "Weak", "weak"
            elif 0 <= score < 2:
                return "Terrible", "terrible"
            else:
                return "N/A", "na"

        def weighted_GPA(gpa, ap_courses):
            wgpa = gpa
            count = ap_courses
            while count > 0:
                wgpa += random.uniform(0, 0.4)  # Adds a random value between 0 and 0.4 for each AP course
                count -= 1
            # Optionally, you might want to cap the WGPA to a maximum value, e.g., 100
            wgpa = min(wgpa, 100.0)
            return round(wgpa, 2)  # Round to two decimal places for consistency
        
        # Compute demographic score and category
        wgpa = weighted_GPA(gpa_val, ap_val)
        dem_score = demScore(gender, race, first_gen)
        dem_category, dem_class = rate(dem_score)

        # Add demographic score and category to submission_data
        submission_data = {
            "name": name,
            "gpa": gpa_val,
            "test_option": test_option,
            "sat_score": sat_val if test_option == 'sat' else None,
            "act_score": act_val if test_option == 'act' else None,
            "extracurriculars": extracurriculars_val,
            "essays": essays_val,
            "ap_courses": ap_val,
            "race": race,       # Stored as integer code
            "gender": gender,   # Stored as integer code
            "first_gen": first_gen,
            "dem_score": dem_score,          # Store Demographic Score
            "dem_category": dem_category,    # Store Demographic Category
            "dem_class": dem_class,          # Store CSS Class for Category
            "wgpa": wgpa  
        }
        submissions.append(submission_data)
        
        # Update session['advancedsim_data'] with submission_data
        if 'advancedsim_data' in session:
            session['advancedsim_data'].update(submission_data)
        else:
            session['advancedsim_data'] = submission_data

        flash("Application submitted successfully!", "success")
        # Redirect to the next step in your application process
        return redirect(url_for("earlydecision"))

    return render_template("advancedsim.html")

# Helper Functions for Session Management
def add_school(school):
    if 'selected_schools' not in session:
        session['selected_schools'] = []
    if school not in session['selected_schools']:
        session['selected_schools'].append(school)
        print(f"Added school: {school}")
    else:
        print(f"School already selected: {school}")
    session.modified = True
    print(f"Current selected_schools: {session['selected_schools']}")

def remove_school(school):
    if 'selected_schools' in session and school in session['selected_schools']:
        session['selected_schools'].remove(school)
        print(f"Removed school: {school}")
    else:
        print(f"School not found in selected_schools: {school}")
    session.modified = True
    print(f"Current selected_schools: {session.get('selected_schools', [])}")
    
def clear_all_schools():
    session.pop('selected_schools', None)
    session.modified = True
    print("Cleared all selected_schools")
    
def clear_session():
    keys_to_clear = [
        'selected_schools',
        'ed_school',
        'rea_school',
        'ea_schools',
        'rd_schools',
        'applied_colleges',
        'interview_chances',
        'advancedsim_data'  # Include if you want to reset all user data
    ]
    for key in keys_to_clear:
        session.pop(key, None)
    print("Session cleared!")

# Early Decision Route
@app.route('/advancedsim/earlydecision', methods=['GET', 'POST'])
@login_required
def earlydecision():
    if 'selected_schools' not in session:
        session['selected_schools'] = []  # Initialize the list to store selected schools

    if request.method == 'POST':
        ed_choice = request.form.get('ed_choice')
        session['ed_choice'] = ed_choice

        if ed_choice == 'yes':  # User selects ED
            ed_school = request.form.get('ed_school')  # Get the selected ED school
            if ed_school:
                session['ed_school'] = ed_school
                add_school(ed_school)  # Add ED school to the list

                # **Clear REA Selection if Exists**
                rea_school = session.get('rea_school')
                if rea_school:
                    remove_school(rea_school)
                    session['rea_school'] = None
                    session['rea_choice'] = 'no'
                    flash("Restrictive Early Action school has been cleared as you selected Early Decision.", "info")

                return redirect(url_for('earlyaction'))  # Skip REA, go to EA
            else:
                flash("Please select an Early Decision school.", "danger")
        else:  # User selects No for ED
            # If previously selected ED, remove it
            ed_school = session.get('ed_school')
            if ed_school:
                remove_school(ed_school)
            session['ed_school'] = None

            return redirect(url_for('rea'))  # Proceed to REA

    if request.method == 'GET':
        # Check if the user is navigating back
        action = request.args.get('action')
        if action == 'back':
            # Clear ED selections
            ed_school = session.get('ed_school')
            if ed_school:
                remove_school(ed_school)
                session['ed_school'] = None
                flash("Early Decision school has been cleared as you navigated back.", "info")
            return redirect(url_for('earlydecision'))  # Redirect to Advanced Sim

    # Filter ED schools: ED available if column[2] != "N"
    ed_schools = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0])
        }
        for u in college_list if u[2] != "N"
    ]

    return render_template('earlydecision.html', ed_schools=ed_schools)

# REA Route
@app.route('/advancedsim/rea', methods=['GET', 'POST'])
@login_required
def rea():
    if request.method == 'POST':
        rea_choice = request.form.get('rea_choice')
        session['rea_choice'] = rea_choice
        if rea_choice == 'yes':
            rea_school = request.form.get('rea_school')  # User selects one REA school
            if rea_school:
                session['rea_school'] = rea_school
                add_school(rea_school)  # Add REA school to the list

                # **Clear ED Selection if Exists**
                ed_school = session.get('ed_school')
                if ed_school:
                    remove_school(ed_school)
                    session['ed_school'] = None
                    session['ed_choice'] = 'no'
                    flash("Early Decision school has been cleared as you selected Restrictive Early Action.", "info")

                return redirect(url_for('earlyaction'))
            else:
                flash("Please select a Restricted Early Action school.", "danger")
        else:
            # If previously selected REA, remove it
            rea_school = session.get('rea_school')
            if rea_school:
                remove_school(rea_school)
            session['rea_school'] = None
            session['rea_choice'] = 'no'
            return redirect(url_for('earlyaction'))

    if request.method == 'GET':
        # Check if the user is navigating back
        action = request.args.get('action')
        if action == 'back':
            # Clear REA selections
            rea_school = session.get('rea_school')
            if rea_school:
                remove_school(rea_school)
                session['rea_school'] = None
                flash("Restrictive Early Action school has been cleared as you navigated back.", "info")
            return redirect(url_for('rea'))  # Redirect to Early Decision

    # Filter REA schools: column[4] == "REA" and u[3] != "N"
    rea_schools = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0])
        }
        for u in college_list if u[4] == "REA" and u[3] != "N"
    ]

    return render_template('rea.html', rea_schools=rea_schools)

# Early Action Route
@app.route('/advancedsim/earlyaction', methods=['GET', 'POST'])
@login_required
def earlyaction():
    if request.method == 'POST':
        ea_choice = request.form.get('ea_choice')
        session['ea_choice'] = ea_choice

        if ea_choice == 'yes':
            ea_schools_selected = request.form.getlist('ea_schools')  # Multiple EA schools

            if not ea_schools_selected:
                flash("Please select at least one Early Action school.", "danger")
                return render_template('earlyaction.html', ea_schools=prepare_ea_schools())

            # Prevent duplicates
            for school in ea_schools_selected:
                add_school(school)

            session['ea_schools'] = ea_schools_selected
            session.modified = True  # Mark session as modified

            flash("Early Action schools selected successfully!", "success")
            return redirect(url_for('regulardecision'))
        else:
            # If previously selected EA schools, remove them
            ea_schools = session.get('ea_schools', [])
            for school in ea_schools:
                remove_school(school)
            session['ea_schools'] = []
            flash("No Early Action schools selected.", "info")
            return redirect(url_for('regulardecision'))

    if request.method == 'GET':
        # Check if the user is navigating back
        action = request.args.get('action')
        if action == 'back':
            # Clear EA selections
            ea_schools = session.get('ea_schools', [])
            for school in ea_schools:
                remove_school(school)
            session['ea_schools'] = []
            flash("Early Action schools have been cleared as you navigated back.", "info")
            return redirect(url_for('earlyaction'))  # Redirect to REA

    chosen_ed = session.get('ed_school')
    chosen_rea = session.get('rea_school')
    chosen_ea = session.get('ea_schools', [])

    # Exclude ED, REA, and already selected EA schools from the list
    excluded_schools = set(filter(None, [chosen_ed, chosen_rea])) | set(chosen_ea)

    # If REA is chosen, only public EA schools and u[3] != "N"
    if chosen_rea:
        filtered_colleges = [
            u for u in college_list 
            if u[0] not in excluded_schools and u[4] == "PUB" and u[3] != "N"
        ]
    else:
        # Show both private (P) and public (PUB) schools not chosen yet and u[3] != "N"
        filtered_colleges = [
            u for u in college_list 
            if u[0] not in excluded_schools and u[4] in ["P", "PUB"] and u[3] != "N"
        ]

    # Prepare EA schools as list of dictionaries
    ea_schools = [
        {
            "name": u[0],
            "display_name": next(
                (uni["display_name"] for uni in university_list if uni["name"] == u[0]), 
                u[0]
            )
        }
        for u in filtered_colleges
    ]

    return render_template('earlyaction.html', ea_schools=ea_schools)

# Helper Function to Prepare EA Schools
def prepare_ea_schools():
    """
    Helper function to prepare EA schools list of dictionaries.
    This ensures consistency and avoids repetition.
    """
    chosen_ed = session.get('ed_school')
    chosen_rea = session.get('rea_school')
    chosen_ea = session.get('ea_schools', [])

    # Exclude ED, REA, and already selected EA schools from the list
    excluded_schools = set(filter(None, [chosen_ed, chosen_rea])) | set(chosen_ea)

    # If REA is chosen, only public EA schools
    if chosen_rea:
        filtered_colleges = [u for u in college_list if u[0] not in excluded_schools and u[4] == "PUB" and u[3] != "N"]
    else:
        # Show both private (P) and public (PUB) schools not chosen yet
        filtered_colleges = [u for u in college_list if u[0] not in excluded_schools and u[4] in ["P", "PUB"] and u[3] != "N"]

    # Prepare EA schools as list of dictionaries
    ea_schools = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0])
        }
        for u in filtered_colleges
    ]

    return ea_schools

# Regular Decision Route
@app.route('/advancedsim/regulardecision', methods=['GET', 'POST'])
@login_required
def regulardecision():
    if request.method == 'POST':
        rd_schools_selected = request.form.getlist('rd_schools')  # Multiple RD schools

        if not rd_schools_selected:
            flash("Please select at least one Regular Decision school.", "danger")
            return render_template('regulardecision.html', rd_schools=prepare_rd_schools())

        # Prevent duplicates
        for school in rd_schools_selected:
            add_school(school)

        session['rd_schools'] = rd_schools_selected
        session.modified = True  # Mark session as modified

        flash("Regular Decision schools selected successfully!", "success")
        return redirect(url_for('summary'))

    if request.method == 'GET':
        # Check if the user is navigating back
        action = request.args.get('action')
        if action == 'back':
            # Clear RD selections
            rd_schools = session.get('rd_schools', [])
            for school in rd_schools:
                remove_school(school)
            session['rd_schools'] = []
            flash("Regular Decision schools have been cleared as you navigated back.", "info")
            return redirect(url_for('regulardecision'))  # Redirect to Early Action

    # GET request logic
    chosen_all = session.get('selected_schools', [])

    # RD shows all not chosen yet in ED/REA/EA/RD and u[3] != "N"
    rd_schools = [u for u in college_list if u[0] not in chosen_all]

    # Prepare RD schools as list of dictionaries with 'name' and 'display_name'
    rd_schools_prepared = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0])
        }
        for u in rd_schools
    ]

    # Debugging: Print available RD schools
    print("Selected Schools:", session.get('selected_schools', []))
    print("RD Schools Available:", rd_schools_prepared)

    return render_template('regulardecision.html', rd_schools=rd_schools_prepared)

# Helper Function to Prepare RD Schools
def prepare_rd_schools():
    """
    Helper function to prepare RD schools list of dictionaries.
    This ensures consistency and avoids repetition.
    """
    chosen_all = session.get('selected_schools', [])

    # RD shows all not chosen yet in ED/REA/EA/RD and u[3] != "N"
    rd_schools = [u for u in college_list if u[0] not in chosen_all]

    # Prepare RD schools as list of dictionaries
    rd_schools_prepared = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0])
        }
        for u in rd_schools
    ]

    # Debugging: Print prepared RD schools
    print("Preparing RD Schools:")
    print(rd_schools_prepared)

    return rd_schools_prepared

def generate_unique_id(short_name, app_type):
    return f"{short_name.lower()}_{app_type.lower()}"


@app.route('/advancedsim/summary')
@login_required
def summary():
    from datetime import datetime

    # Retrieve user data
    user_data = session.get('advancedsim_data', {})
    user_profile = {
        "Name": user_data.get("name", "N/A"),
        "GPA": user_data.get("gpa", "N/A"),
        "Test Option": user_data.get("test_option", "N/A").upper(),
        "SAT Score": user_data.get("sat_score", "N/A") if user_data.get("test_option") == 'sat' else "N/A",
        "ACT Score": user_data.get("act_score", "N/A") if user_data.get("test_option") == 'act' else "N/A",
        "Extracurricular Activities": user_data.get("extracurriculars", "N/A"),
        "Essays Rating": user_data.get("essays", "N/A"),
        "AP Courses Taken": user_data.get("ap_courses", "N/A"),
        "Race/Ethnicity": user_data.get("race", "N/A"),
        "Gender": user_data.get("gender", "N/A"),
        "First Generation": "Yes" if user_data.get("first_gen") else "No",
        "Demographic Score": user_data.get("dem_score", "N/A"),
        "Demographic Category": user_data.get("dem_category", "N/A"),
        "Demographic Class": user_data.get("dem_class", "na"),
        "Weighted GPA": user_data.get("wgpa", "N/A")
    }

    # Gather the applied colleges
    applied_colleges = []

    # Check for ED
    ed_school = session.get('ed_school')
    if ed_school:
        c_entry = next((col for col in college_list if col[0].lower() == ed_school.lower()), None)
        uni_info = next((uni for uni in university_list if uni["name"].lower() == ed_school.lower()), None)
        if c_entry and uni_info:
            applied_colleges.append({
                "app_type": "ED",
                "short_name": c_entry[0].lower(),
                "display_name": uni_info["display_name"],
                "logo_url": uni_info["logo"],
                "public": "Public" if c_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Check for REA
    rea_school = session.get('rea_school')
    if rea_school:
        c_entry = next((col for col in college_list if col[0].lower() == rea_school.lower()), None)
        uni_info = next((uni for uni in university_list if uni["name"].lower() == rea_school.lower()), None)
        if c_entry and uni_info:
            applied_colleges.append({
                "app_type": "REA",
                "short_name": c_entry[0].lower(),
                "display_name": uni_info["display_name"],
                "logo_url": uni_info["logo"],
                "public": "Public" if c_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Check for EA
    ea_schools = session.get('ea_schools', [])
    for ea_school_name in ea_schools:
        c_entry = next((col for col in college_list if col[0].lower() == ea_school_name.lower()), None)
        uni_info = next((uni for uni in university_list if uni["name"].lower() == ea_school_name.lower()), None)
        if c_entry and uni_info:
            applied_colleges.append({
                "app_type": "EA",
                "short_name": c_entry[0].lower(),
                "display_name": uni_info["display_name"],
                "logo_url": uni_info["logo"],
                "public": "Public" if c_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Check for RD
    rd_schools = session.get('rd_schools', [])
    for rd_school_name in rd_schools:
        c_entry = next((col for col in college_list if col[0].lower() == rd_school_name.lower()), None)
        uni_info = next((uni for uni in university_list if uni["name"].lower() == rd_school_name.lower()), None)
        if c_entry and uni_info:
            applied_colleges.append({
                "app_type": "RD",
                "short_name": c_entry[0].lower(),
                "display_name": uni_info["display_name"],
                "logo_url": uni_info["logo"],
                "public": "Public" if c_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Sort by type
    type_order = {"ED": 1, "REA": 2, "EA": 3, "RD": 4}
    applied_colleges.sort(key=lambda x: type_order.get(x["app_type"], 5))

    session['applied_colleges'] = applied_colleges
    print("Summary - Applied Colleges:", applied_colleges)

    # Build decisions_queue
    decisions_queue = []
    for college in applied_colleges:
        short_name = college['short_name']
        display_name = college['display_name']
        app_type = college['app_type'].upper()  # "ED", "EA", "REA", or "RD"
        logo_url = college['logo_url']

        # Find the row in college_list
        c_entry = next((c for c in college_list if c[0].lower() == short_name.lower()), None)
        if not c_entry:
            print(f"College '{short_name}' not found in college_list.")
            continue

        # Determine release date index
        if app_type == "ED" or app_type == "REA":
            # c_entry[5] = ED/REA release date
            rdate = c_entry[5] if len(c_entry) > 5 and c_entry[5] != "N" else "2099-01-01"
        elif app_type == "EA":
            # c_entry[6] = EA release date
            rdate = c_entry[6] if len(c_entry) > 6 and c_entry[6] != "N" else "2099-01-01"
        else:
            # RD
            rdate = c_entry[7] if len(c_entry) > 7 and c_entry[7] != "N" else "2099-01-01"

        unique_id = generate_unique_id(short_name, app_type)
        decisions_queue.append({
            "short_name": short_name,
            "unique_id": unique_id,
            "display_name": display_name,
            "app_type": app_type,
            "release_date": rdate,
            "formatted_release_date": format_date(rdate),
            "logo_url": logo_url
        })

    # Sort decisions by date
    try:
        decisions_queue_sorted = sorted(
            decisions_queue,
            key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d')
        )
    except ValueError:
        decisions_queue_sorted = decisions_queue

    final_results = session.get('final_results', {})

    # Update final_results with correct release_date
    for dec in decisions_queue_sorted:
        unique_id = dec['unique_id']
        if unique_id not in final_results:
            final_results[unique_id] = {
                'decision_code': 'R',
                'app_type': dec['app_type'],
                'release_date': dec['release_date']
            }
        else:
            # Overwrite with correct date
            final_results[unique_id]['release_date'] = dec['release_date']

    session['final_results'] = final_results
    session['decisions_queue_sorted'] = decisions_queue_sorted

    return render_template(
        'summary.html',
        user_profile=user_profile,
        applied_colleges=applied_colleges,
        decisions_queue=decisions_queue_sorted
    )

# helper functions for chancing
def sim10():
    var1 = random.uniform(0, 10)
    if var1 < 1:
        var2 = random.uniform(0, 2)
    elif var1 < 3:
        var2 = random.uniform(0, 5.5)
    elif var1 < 5:
        var2 = random.uniform(0, 9)
    elif var1 < 7:
        var2 = 2 + random.uniform(0, 8)
    elif var1 < 9:
        var2 = 3 + random.uniform(0, 8)
    else:
        var2 = 9 + random.uniform(0, 1.2)

    if var2 > 10:
        var2 = 10.0
    if var2 < 5:
        if var2 <= 1:
            var2 += random.uniform(0, 1.5)
        var2 = var2 - 1 + random.uniform(0, 2.5)
    if var2 < 0:
        var2 = 0.0

    return round(var2, 2)

def getType(chance):
    if chance > 80:
        return "Safety", "safety"
    elif chance > 65:
        return "Highly Likely", "highly-likely"
    elif chance > 45:
        return "Target", "target"
    elif chance > 30:
        return "Hard Target", "hard-target"
    elif chance > 21:
        return "Competitive", "competitive"
    elif chance > 12:
        return "Reach", "reach"
    elif chance > 5:
        return "Big Reach", "big-reach"
    else:
        return "Huge Reach", "huge-reach"

def classify(student_num):
    # Define classification based on student_num
    # Assuming student_num ranges from 0 to 100, map to tier 1-10
    if student_num >= 92:
        return 1
    elif student_num >= 84:
        return 2
    elif student_num >= 77:
        return 3
    elif student_num >= 68:
        return 4
    elif student_num >= 61:
        return 5
    elif student_num >= 54:
        return 6
    elif student_num >= 48:
        return 7
    elif student_num >= 40:
        return 8
    elif student_num >= 29:
        return 9
    else:
        return 10
    
def chanceCollege(collegeList, i, demScore, testOptional, sat, act, extracurriculars, ap_courses, essayStrength, gpa, interviewStrength, app_type):
    baseChance = float(collegeList[i][1]) * 100  # Acceptance rate as percentage (0-100)
    interviewScore = interviewStrength

    student_num = 0.0
    if testOptional:
        # GPA = 40 pts, EC = 20 pts, Essay = 15 pts, AP = 10 pts, Interview = 15 pts
        if gpa > 99:
            student_num += 40
        elif gpa > 98:
            student_num += 39
        elif gpa > 97:
            student_num += 38
        elif gpa > 96:
            student_num += 36
        elif gpa > 95:
            student_num += 34
        elif gpa > 94:
            student_num += 32
        elif gpa > 93:
            student_num += 29
        elif gpa > 92:
            student_num += 26.5
        elif gpa > 91:
            student_num += 25
        elif gpa > 90:
            student_num += 22
        elif gpa > 88:
            student_num += 21
        elif gpa > 85:
            student_num += 16
        elif gpa > 82.5:
            student_num += 13
        elif gpa > 80:
            student_num += 11
        elif gpa > 75:
            student_num += 8
        elif gpa > 70:
            student_num += 5
        else:
            student_num += 2
        student_num += extracurriculars * 2
        student_num += ap_courses * 0.9
        student_num += interviewScore * 1.6
        student_num += essayStrength * 1.5
    else:
        # GPA = 35 pts, EC = 15 pts, Essay = 15 pts, AP = 10 pts, Interview = 10 pts, SAT/ACT = 15 pts
        if gpa > 99:
            student_num += 35
        elif gpa > 98:
            student_num += 34
        elif gpa > 97:
            student_num += 33
        elif gpa > 96:
            student_num += 32
        elif gpa > 95:
            student_num += 30
        elif gpa > 94:
            student_num += 28
        elif gpa > 93:
            student_num += 26
        elif gpa > 92:
            student_num += 24
        elif gpa > 91:
            student_num += 22
        elif gpa > 90:
            student_num += 20
        elif gpa > 88:
            student_num += 18
        elif gpa > 85:
            student_num += 15
        elif gpa > 82.5:
            student_num += 12
        elif gpa > 80:
            student_num += 10
        elif gpa > 75:
            student_num += 7
        elif gpa > 70:
            student_num += 5
        else:
            student_num += 3

        student_num += extracurriculars * 1.5
        student_num += ap_courses * 0.9
        student_num += interviewScore * 1.25
        student_num += essayStrength * 1

        # SAT/ACT contribution (15 pts max)
        if sat != -1:
            if sat == 1600:
                student_num += 15
            elif sat >= 1570:
                student_num += 14
            elif sat >= 1540:
                student_num += 13
            elif sat >= 1510:
                student_num += 11.5
            elif sat >= 1490:
                student_num += 10.5
            elif sat >= 1450:
                student_num += 9
            elif sat >= 1400:
                student_num += 6
            elif sat >= 1300:
                student_num += 3
            else:
                student_num += 1
        elif act != -1:
            if act == 36:
                student_num += 15
            elif act >= 35:
                student_num += 14
            elif act >= 34:
                student_num += 13
            elif act >= 33:
                student_num += 12
            elif act >= 32:
                student_num += 11
            elif act >= 31:
                student_num += 10
            elif act >= 30:
                student_num += 9
            elif act >= 29:
                student_num += 7
            elif act >= 27:
                student_num += 5
            elif act >= 25:
                student_num += 3
            elif act >= 23:
                student_num += 2
            else:
                student_num += 1

    if demScore > 5:
        student_num += (demScore - 5)
    else:
        student_num -= (5 - demScore)

    tier = classify(student_num)
    chances = 0

    if baseChance < 5:  # <5%
        if tier == 1:
            chances = 34 + random.uniform(-3, 2)  # 36 + (random *8 -4 -2)
        elif tier == 2:
            chances = 24 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 19 + random.uniform(-4, 2)
        elif tier == 4:
            chances = 11 + random.uniform(-5, 1)
        elif tier == 5:
            chances = 4 + random.uniform(-3, 3)
        elif tier == 6:
            chances = 2 + random.uniform(-3, 3)
        elif tier == 7:
            chances = 1 + random.uniform(-1, 1)
        elif tier == 8:
            chances = 0.5 + random.uniform(-0.2, 0.2)
        elif tier == 9:
            chances = 0.2 + random.uniform(-0.1, 0.1)
        elif tier == 10:
            chances = 0.1
        else:
            chances = 0.05
    elif baseChance < 10:  # <10%
        if tier == 1:
            chances = 44 + random.uniform(-6, 2)  # 46 + (random *8 -4 -2)
        elif tier == 2:
            chances = 31 + random.uniform(-6, 2)
        elif tier == 3:
            chances = 23 + random.uniform(-6, 2)
        elif tier == 4:
            chances = 16 + random.uniform(-5, 1)
        elif tier == 5:
            chances = 10 + random.uniform(-3, 3)
        elif tier == 6:
            chances = 6 + random.uniform(-3, 3)
        elif tier == 7:
            chances = 2 + random.uniform(-1, 1)
        elif tier == 8:
            chances = 0.5 + random.uniform(-0.2, 0.2)
        elif tier == 9:
            chances = 0.2 + random.uniform(-0.1, 0.1)
        elif tier == 10:
            chances = 0.1
        else:
            chances = 0.05
    elif baseChance < 16:  # <16%
        if tier == 1:
            chances = 54 + random.uniform(-6, 2)
        elif tier == 2:
            chances = 41 + random.uniform(-5, 2)
        elif tier == 3:
            chances = 32 + random.uniform(-5, 2)
        elif tier == 4:
            chances = 23 + random.uniform(-5, 2)
        elif tier == 5:
            chances = 18 + random.uniform(-5, 2)
        elif tier == 6:
            chances = 11 + random.uniform(-5, 2)
        elif tier == 7:
            chances = 5 + random.uniform(-3, 0)
        elif tier == 8:
            chances = 3 + random.uniform(-2.2, 0)
        elif tier == 9:
            chances = 2 + random.uniform(-0.1, 0.1)
        elif tier == 10:
            chances = 1 + random.uniform(-0.1, 0.1)
        else:
            chances = 0.5 + random.uniform(-0.05, 0.05)
    elif baseChance < 25:  # <25%
        if tier == 1:
            chances = 63 + random.uniform(-5, 5)
        elif tier == 2:
            chances = 52 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 38 + random.uniform(-3, 2)
        elif tier == 4:
            chances = 31 + random.uniform(-3, 2)
        elif tier == 5:
            chances = 23 + random.uniform(-3, 2)
        elif tier == 6:
            chances = 17 + random.uniform(-3, 2)
        elif tier == 7:
            chances = 11 + random.uniform(-3, 2)
        elif tier == 8:
            chances = 6 + random.uniform(-3, 2)
        elif tier == 9:
            chances = 3 + random.uniform(-3, 2)
        elif tier == 10:
            chances = 2 + random.uniform(-0.1, 0.1)
        else:
            chances = 0.7 + random.uniform(-0.05, 0.05)
    elif baseChance < 35:  # <35%
        if tier == 1:
            chances = 71 + random.uniform(-5, 5)
        elif tier == 2:
            chances = 63 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 55 + random.uniform(-4, 2)
        elif tier == 4:
            chances = 44 + random.uniform(-4, 2)
        elif tier == 5:
            chances = 36 + random.uniform(-4, 2)
        elif tier == 6:
            chances = 31 + random.uniform(-4, 2)
        elif tier == 7:
            chances = 23 + random.uniform(-4, 2)
        elif tier == 8:
            chances = 17 + random.uniform(-4, 2)
        elif tier == 9:
            chances = 14 + random.uniform(-4, 2)
        elif tier == 10:
            chances = 7 + random.uniform(-4, 2)
        else:
            chances = 3 + random.uniform(-1, 1) - 2
    elif baseChance < 45:  # <45%
        if tier == 1:
            chances = 79 + random.uniform(-5, 5)
        elif tier == 2:
            chances = 70 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 64 + random.uniform(-4, 2)
        elif tier == 4:
            chances = 58 + random.uniform(-4, 2)
        elif tier == 5:
            chances = 47 + random.uniform(-4, 2)
        elif tier == 6:
            chances = 40 + random.uniform(-4, 2)
        elif tier == 7:
            chances = 34 + random.uniform(-4, 2)
        elif tier == 8:
            chances = 27 + random.uniform(-4, 2)
        elif tier == 9:
            chances = 20 + random.uniform(-4, 2)
        elif tier == 10:
            chances = 13 + random.uniform(-4, 2)
        else:
            chances = 5 + random.uniform(-0.1, 0.1) - 2
    elif baseChance < 60:  # <60%
        if tier == 1:
            chances = 81 + random.uniform(-6, 2)
        elif tier == 2:
            chances = 74 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 67 + random.uniform(-4, 2)
        elif tier == 4:
            chances = 62 + random.uniform(-4, 2)
        elif tier == 5:
            chances = 53 + random.uniform(-4, 2)
        elif tier == 6:
            chances = 46 + random.uniform(-4, 2)
        elif tier == 7:
            chances = 36 + random.uniform(-5, 2)
        elif tier == 8:
            chances = 25 + random.uniform(-4, 2)
        elif tier == 9:
            chances = 16 + random.uniform(-3, 2)
        elif tier == 10:
            chances = 7 + random.uniform(-3, 2)
        else:
            chances = 3 + random.uniform(-1, 1) - 2
    elif baseChance < 80:  # <80%
        if tier == 1:
            chances = 86 + random.uniform(-6, 2)
        elif tier == 2:
            chances = 81 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 74 + random.uniform(-4, 2)
        elif tier == 4:
            chances = 69 + random.uniform(-4, 2)
        elif tier == 5:
            chances = 63 + random.uniform(-4, 2)
        elif tier == 6:
            chances = 56 + random.uniform(-4, 2)
        elif tier == 7:
            chances = 45 + random.uniform(-5, 2)
        elif tier == 8:
            chances = 37 + random.uniform(-4, 2)
        elif tier == 9:
            chances = 28 + random.uniform(-3, 2)
        elif tier == 10:
            chances = 24 + random.uniform(-3, 2)
        else:
            chances = 18 + random.uniform(-1, 1) - 2
    else:
        # baseChance >=80%
        if tier == 1:
            chances = 93 + random.uniform(-6, 2)
        elif tier == 2:
            chances = 87 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 80 + random.uniform(-4, 2)
        elif tier == 4:
            chances = 74 + random.uniform(-4, 2)
        elif tier == 5:
            chances = 65 + random.uniform(-4, 2)
        elif tier == 6:
            chances = 56 + random.uniform(-4, 2)
        elif tier == 7:
            chances = 45 + random.uniform(-5, 2)
        elif tier == 8:
            chances = 37 + random.uniform(-4, 2)
        elif tier == 9:
            chances = 28 + random.uniform(-3, 2)
        elif tier == 10:
            chances = 24 + random.uniform(-3, 2)
        else:
            chances = 18 + random.uniform(-1, 1) - 2

    # Application type adjustments
    if app_type == "ED" and collegeList[i][2] != "N":
        chances *= float(collegeList[i][2])
    if app_type in ["EA", "REA"] and collegeList[i][3] != "N":
        chances *= float(collegeList[i][3])
        
    # georgetown needs 95+
    if collegeList[i][0] == "georgetown":
        if gpa < 93:
            chances /= random.uniform(1.2, 2.4)
        if gpa > 96.5:
            chances *= random.uniform(1.2, 2.4)

    chances += random.uniform(-2, 2)  # Simulating chances -= Math.random()*4 -1

    if interviewScore < 2:
        chances -= random.uniform(0, 7)
    if interviewScore > 8:
        chances += random.uniform(0, 7)
    if chances <= 0.0:
        chances = 0.0
        chances += random.uniform(0, 1.5)
    if chances >= 100.0:
        chances = 100.0
        chances -= random.uniform(0, 3)
    if chances >= 97:
        chances -= random.uniform(0, 6)

    # if (chances <= 10):
    #    chances *= random.uniform(1, 1.7)
    if chances > 95:
        chances -= random.uniform(0, 8)
    chances -= random.uniform(0, 10)
    chances = max(0.0, min(chances, 100.0))
    return round(chances, 2)

def rate(score):
    if 8.7 <= score <= 10:
        return "Outstanding", "outstanding"
    elif 7.2 <= score < 8.7:
        return "Strong", "strong"
    elif 6 <= score < 7.2:
        return "Moderate", "moderate"
    elif 4.5 <= score < 6:
        return "Fair", "fair"
    elif 2 <= score < 4.5:
        return "Weak", "weak"
    elif 0 <= score < 2:
        return "Terrible", "terrible"
    else:
        return "N/A", "na"

@app.route('/advancedsim/chances', methods=["GET", "POST"])
@login_required
def chances():
    # Clear previous simulation state
    session.pop('read_emails', None)
    session.pop('current_sim_date', None)
    session.pop('simulation_started', None)
    session.pop('final_results', None)
    session.pop('deferred_decisions', None)
    session.pop('opened_colleges', None)
    session.pop('decisions_queue_sorted', None)

    if request.method == 'POST':
        flash("Chances reviewed successfully!", "success")
        applied_colleges = session.get('applied_colleges', [])
        interview_chances = session.get('interview_chances', {})

        # Retrieve or initialize final_results & decisions_queue_sorted
        final_results = session.get('final_results', {})
        decisions_queue_sorted = session.get('decisions_queue_sorted', [])

        if not decisions_queue_sorted:
            # Build decisions_queue_sorted and initialize final_results
            new_queue = []
            for college in applied_colleges:
                short_name = college['short_name']
                app_type = college['app_type'].upper()

                # Retrieve simulation data from college_list
                c_entry_sim = next((c for c in college_list if c[0].lower() == short_name.lower()), None)
                if not c_entry_sim:
                    continue

                # Retrieve display data from university_list
                c_entry_display = next((c for c in university_list if c["name"].lower() == short_name.lower()), None)
                if not c_entry_display:
                    continue

                # Determine school_type
                school_type = "Public" if c_entry_sim[4].upper() in ["PUB", "P"] else "Private"

                # Decide which date column to pick based on app_type
                if app_type in ["ED", "REA"]:
                    rdate = c_entry_sim[5] if len(c_entry_sim) > 5 and c_entry_sim[5] != "N" else "2099-01-01"
                elif app_type == "EA":
                    rdate = c_entry_sim[6] if len(c_entry_sim) > 6 and c_entry_sim[6] != "N" else "2099-01-01"
                else:  # RD
                    rdate = c_entry_sim[7] if len(c_entry_sim) > 7 and c_entry_sim[7] != "N" else "2099-01-01"

                unique_id = generate_unique_id(short_name, app_type)
                new_queue.append({
                    "short_name": short_name.lower(),
                    "unique_id": unique_id,
                    "display_name": c_entry_display["display_name"],
                    "app_type": app_type,
                    "release_date": rdate,
                    "logo_url": c_entry_display.get("logo", "static/logos/default-logo.jpg"),
                    "school_type": school_type
                })

                if unique_id not in final_results:
                    final_results[unique_id] = {
                        'decision_code': 'R',
                        'app_type': app_type,
                        'release_date': rdate
                    }

            # Sort by date if possible
            try:
                new_queue.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
            except ValueError:
                pass

            session['decisions_queue_sorted'] = new_queue
            decisions_queue_sorted = new_queue
            session['final_results'] = final_results

        #
        # 1) Generate *early-round* decisions via admissionsDecision
        #
        for unique_id, data in interview_chances.items():
            # e.g., unique_id = 'duke_ed'
            try:
                college_short_name, unique_app_type = unique_id.rsplit('_', 1)
            except ValueError:
                print(f"Invalid unique_id format: {unique_id}")
                continue

            # Retrieve simulation data
            c_entry_sim = next((c for c in college_list if c[0].lower() == college_short_name.lower()), None)
            if not c_entry_sim:
                continue

            # Retrieve display data
            c_entry_display = next((c for c in university_list if c["name"].lower() == college_short_name.lower()), None)
            if not c_entry_display:
                continue

            idx = college_list.index(c_entry_sim)
            uppercase_app_type = unique_app_type.upper()
            chances_val = data.get('chances', 50.0)

            # admissionsDecision for ED/EA/REA (or RD if user applied RD initially)
            decision_code = admissionsDecision(
                chances=chances_val,
                appType=uppercase_app_type,
                idx=idx,
                college_list=college_list,
                decisions_queue_sorted=decisions_queue_sorted
            )

            # Overwrite final_results with new code
            if uppercase_app_type == "RD":
                release_date = c_entry_sim[7] if len(c_entry_sim) > 7 else "2099-01-01"
            elif uppercase_app_type == "EA":
                release_date = c_entry_sim[6] if len(c_entry_sim) > 6 else "2099-01-01"
            else:  # ED or REA
                release_date = c_entry_sim[5] if len(c_entry_sim) > 5 else "2099-01-01"

            final_results[unique_id] = {
                'decision_code': decision_code,
                'app_type': uppercase_app_type,
                'release_date': release_date
            }

        #
        # 2) Now handle newly created RD placeholders from deferral
        #    (They were scheduled with 'decision_code' == 'PENDING'.)
        #
        locked_until_opened = session.get('locked_until_opened', {})
        for uid, info in list(final_results.items()):
            if info.get('decision_code') == "PENDING" and info.get('app_type') == "RD":
                # This is the RD "placeholder" created due to deferral.
                # Let's recompute chances using RD parameters and the original interview strength.
                try:
                    college_short_name, _ = uid.rsplit('_', 1)  # e.g., "duke_rd"
                except ValueError:
                    print(f"Invalid unique_id format for RD: {uid}")
                    continue

                c_entry_sim = next((c for c in college_list if c[0].lower() == college_short_name.lower()), None)
                if not c_entry_sim:
                    continue
                idx = college_list.index(c_entry_sim)

                # Get the initial unique_id that this RD is locked behind
                initial_uid = locked_until_opened.get(uid)
                if not initial_uid:
                    print(f"No initial unique_id found for RD unique_id: {uid}")
                    continue

                # Get the interview_strength from the initial unique_id's interview_chances
                interview_strength = interview_chances.get(initial_uid, {}).get('interview_score', sim10())

                # Retrieve user data to recompute chances
                user_data = session.get('advancedsim_data', {})
                demScore = user_data.get('dem_score', 0.0)
                testOption = user_data.get('test_option', 'rd').lower()
                testOptional = (testOption == 'optional')
                sat = user_data.get('sat_score', -1) or -1
                act = user_data.get('act_score', -1) or -1
                extracurriculars = user_data.get('extracurriculars', 0)
                ap_courses = user_data.get('ap_courses', 0)
                essayStrength = user_data.get('essays', 0)
                gpa = user_data.get('gpa', 0.0)

                # Recompute chances_val_rd using 'app_type'='RD' and reused interview_strength
                chances_val_rd = chanceCollege(
                    collegeList=college_list,
                    i=idx,
                    demScore=demScore,
                    testOptional=testOptional,
                    sat=int(sat),
                    act=int(act),
                    extracurriculars=int(extracurriculars),
                    ap_courses=int(ap_courses),
                    essayStrength=int(essayStrength),
                    gpa=float(gpa),
                    interviewStrength=interview_strength,  # Reuse the initial interview strength
                    app_type="RD"
                )

                # Call admissionsDecision with is_deferred=True to get D/A, D/W, or D/R
                new_code = admissionsDecision(
                    chances=chances_val_rd,
                    appType="RD",
                    idx=idx,
                    college_list=college_list,
                    decisions_queue_sorted=decisions_queue_sorted,
                    is_deferred=True
                )

                # Update final_results with the new decision code
                final_results[uid]['decision_code'] = new_code

        # Update the session with final_results
        session['final_results'] = final_results

        return redirect(url_for('results'))

    #
    # GET: show the chances page
    #
    user_data = session.get('advancedsim_data', {})
    applied_colleges = session.get('applied_colleges', [])
    if not applied_colleges:
        flash("No applied colleges found for advanced simulation.", "warning")
        return redirect(url_for('summary'))

    demScore = user_data.get('dem_score', 0.0)
    testOption = user_data.get('test_option', 'rd').lower()
    testOptional = (testOption == 'optional')
    sat = user_data.get('sat_score', -1) or -1
    act = user_data.get('act_score', -1) or -1
    extracurriculars = user_data.get('extracurriculars', 0)
    ap_courses = user_data.get('ap_courses', 0)
    essayStrength = user_data.get('essays', 0)
    gpa = user_data.get('gpa', 0.0)

    # Build interview_chances
    interview_chances = {}
    for college in applied_colleges:
        short_name = college['short_name']
        app_type = college['app_type'].upper()

        c_entry_sim = next((c for c in college_list if c[0].lower() == short_name.lower()), None)
        if not c_entry_sim:
            continue

        c_entry_display = next((c for c in university_list if c["name"].lower() == short_name.lower()), None)
        if not c_entry_display:
            continue

        school_type = "Public" if c_entry_sim[4].upper() in ["PUB", "P"] else "Private"
        idx = college_list.index(c_entry_sim)

        interview_score = sim10()  # Generate interview strength
        chances_val = chanceCollege(
            collegeList=college_list,
            i=idx,
            demScore=demScore,
            testOptional=testOptional,
            sat=int(sat),
            act=int(act),
            extracurriculars=int(extracurriculars),
            ap_courses=int(ap_courses),
            essayStrength=int(essayStrength),
            gpa=float(gpa),
            interviewStrength=interview_score,
            app_type=app_type
        )

        # Determine interview score category
        chance_category, chance_class = rate(interview_score)
        # Determine overall chances category
        chance_type_label, chance_type_class = getType(chances_val)

        unique_id = generate_unique_id(short_name, app_type)
        interview_chances[unique_id] = {
            "display_name": c_entry_display["display_name"],
            "chances": chances_val,
            "app_type": app_type,
            "logo_url": c_entry_display.get("logo", "static/logos/default-logo.jpg"),
            "interview_score": interview_score,
            "chance_category": chance_category,
            "chance_class": chance_class,
            "chance_type_label": chance_type_label,
            "chance_type_class": chance_type_class,
            "school_type": school_type
        }

    session['interview_chances'] = interview_chances
    return render_template("chances.html", interview_chances=interview_chances)

# admissionsDecision Function
def admissionsDecision(chances, appType, idx, college_list, decisions_queue_sorted, is_deferred=False):
    """
    Determine the admission decision for a given college index in college_list,
    based on 'chances' (0-100), the 'appType' (ED, EA, REA, or RD), and whether
    it's the final (deferred) round or not.
    """
    session.setdefault('final_results', {})
    
    yourFate = min(random.random() * 100, random.random() * 100) + random.random() * 30
    collegeName = college_list[idx][0].lower()

    print(f"Admissions Decision for {collegeName}:")
    print(f"App Type: {appType}, Chances: {chances}, Fate: {yourFate}")

    # Identify the correct release date from the college_list
    if appType == "ED" or appType == "REA":
        release_date_str = college_list[idx][5] if len(college_list[idx]) > 5 else "2099-01-01"
    elif appType == "EA":
        release_date_str = college_list[idx][6] if len(college_list[idx]) > 6 else "2099-01-01"
    else:  # RD
        release_date_str = college_list[idx][7] if len(college_list[idx]) > 7 else "2099-01-01"

    # Now decide
    if appType == "ED":
        if yourFate < chances:
            decision = "ED"  # ED Acceptance
        elif yourFate < chances + random.random() * 30:
            decision = "D"   # Deferred to RD
        else:
            decision = "R"

    elif appType == "REA":
        if yourFate < chances:
            decision = "A"
        elif yourFate < chances + random.random() * 40:
            decision = "D"
        else:
            decision = "R"

    elif appType == "EA":
        if yourFate < chances:
            decision = "A"
        elif yourFate < chances + random.random() * 45:
            decision = "D"
        else:
            decision = "R"

    elif appType == "RD":
        if is_deferred:
            # This is the final outcome after a deferral from ED/EA/REA
            if yourFate < chances:
                decision = "D/A"  # "Deferred -> Accepted"
            elif yourFate < chances + random.random() * 25:
                decision = "D/W"  # "Deferred -> Waitlist"
            else:
                decision = "D/R"  # "Deferred -> Rejected"
        else:
            # Normal RD
            if yourFate < chances:
                decision = "A"
            elif yourFate < chances + random.random() * 25:
                decision = "W"
            else:
                decision = "R"
    else:
        decision = "NO"
        print(f"Unknown application type: {appType}")

    unique_id = generate_unique_id(collegeName, appType)

    # Store the primary outcome in final_results
    session['final_results'][unique_id] = {
        'decision_code': decision,
        'app_type': appType,
        'release_date': release_date_str
    }

    # If early round => user is "D" => schedule new RD record
    if decision == "D" and appType in ["ED", "EA", "REA"] and not is_deferred:
        schedule_deferred_decision(collegeName, appType, college_list, decisions_queue_sorted)

    print(f"Decision: {decision} with date {release_date_str}")
    return decision

def generate_final_decision(college_unique_id):
    chances_val = get_final_chances(college_unique_id)
    college_index = get_college_index(college_unique_id)
    
    if college_index == -1:
        # College not found, default to Rejected
        return "R"
    
    final_decision = admissionsDecision(
        chances=chances_val,
        appType="RD",
        collegeIndex=college_index,
        collegesApplied=college_list,
        decisions_queue_sorted=session.get('decisions_queue_sorted', [])
    )
    
    return final_decision

def get_final_chances(college_unique_id):
    interview_chances = session.get('interview_chances', {})
    if college_unique_id.lower() in interview_chances:
        return interview_chances[college_unique_id.lower()].get('chances', 50.0)
    return 50.0  # Default chance if not found

def get_college_index(college_unique_id):
    for index, college in enumerate(college_list):
        unique_id = f"{college[0].lower()}_{college[4].lower()}"  # Assuming app_type is at index 4
        if unique_id == college_unique_id.lower():
            return index
    return -1  # Not found

def schedule_deferred_decision(college_short_name, early_app_type, college_list, decisions_queue_sorted):
    """
    Creates a new RD unique_id with 'D/R' as the initial placeholder code (meaning "Deferred Rejected").
    The user will later get a final outcome (D/A, D/W, or D/R) after calling admissionsDecision(...) again with is_deferred=True.
    """
    college_entry = next((c for c in college_list if c[0].lower() == college_short_name.lower()), None)
    if not college_entry:
        print(f"College '{college_short_name}' not found in college_list.")
        return

    # The RD date is in column 7
    rd_release_date = "2099-01-01"
    if len(college_entry) > 7 and college_entry[7] != "N":
        rd_release_date = college_entry[7]

    rd_unique_id = f"{college_short_name.lower()}_rd"
    early_uid = f"{college_short_name.lower()}_{early_app_type.lower()}"

    if 'locked_until_opened' not in session:
        session['locked_until_opened'] = {}
    # Lock the RD record behind the early record
    session['locked_until_opened'][rd_unique_id] = early_uid

    final_results = session.setdefault('final_results', {})

    # If not already created, create the new RD entry with a placeholder code
    if rd_unique_id not in final_results:
        final_results[rd_unique_id] = {
            'decision_code': 'PENDING',  # default guess
            'app_type': 'RD',
            'release_date': rd_release_date
        }

    # Insert a new item into decisions_queue_sorted for the RD round
    rd_item = {
        "short_name": college_short_name.lower(),
        "unique_id": rd_unique_id,
        "display_name": next(
            (uni["display_name"] for uni in university_list if uni["name"].lower() == college_short_name.lower()),
            college_short_name.capitalize()
        ),
        "app_type": "RD",
        "release_date": rd_release_date,
        "formatted_release_date": format_date(rd_release_date),
        "logo_url": next(
            (uni["logo"] for uni in university_list if uni["name"].lower() == college_short_name.lower()),
            "static/logos/default-logo.jpg"
        )
    }
    decisions_queue_sorted.append(rd_item)

    # Resort by date
    try:
        from datetime import datetime
        decisions_queue_sorted.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
    except ValueError:
        pass

    session['final_results'] = final_results
    session['decisions_queue_sorted'] = decisions_queue_sorted
    session.modified = True

    print(f"Scheduled new RD record for {college_short_name.upper()} with code 'D/R' and date {rd_release_date}")

@app.route('/advancedsim/results', methods=["GET", "POST"])
@login_required
def results():
    from datetime import datetime

    # Retrieve user data from session
    user_data = session.get('advancedsim_data', {"name": "User"})
    name = user_data.get("name", "User")

    # Retrieve applied colleges and simulation results from session
    applied_colleges = session.get('applied_colleges', [])
    final_results = session.get('final_results', {})
    decisions_queue_sorted = session.get('decisions_queue_sorted', [])
    opened_colleges = session.get('opened_colleges', [])
    locked_until_opened = session.get('locked_until_opened', {})

    print("DEBUG: Currently opened colleges:", opened_colleges)

    # Step 1: Build or Rebuild the Decisions Queue
    if not decisions_queue_sorted:
        new_queue = []
        for college in applied_colleges:
            short_name = college['short_name']
            app_type = college['app_type'].upper()
            c_entry = next((c for c in college_list if c[0].lower() == short_name.lower()), None)
            if not c_entry:
                continue

            # Determine release date based on application type
            if app_type in ["ED", "REA"]:
                rdate = c_entry[5] if len(c_entry) > 5 and c_entry[5] != "N" else "2099-01-01"
            elif app_type == "EA":
                rdate = c_entry[6] if len(c_entry) > 6 and c_entry[6] != "N" else "2099-01-01"
            else:
                rdate = c_entry[7] if len(c_entry) > 7 and c_entry[7] != "N" else "2099-01-01"

            unique_id = generate_unique_id(short_name, app_type)
            new_queue.append({
                "short_name": short_name,
                "unique_id": unique_id,
                "display_name": college['display_name'],
                "app_type": app_type,
                "release_date": rdate,
                "formatted_release_date": format_date(rdate),
                "logo_url": college.get('logo_url', 'static/logos/default-logo.jpg')
            })

            # Initialize final_results if not present
            if unique_id not in final_results:
                final_results[unique_id] = {
                    'decision_code': 'R',  # Default to Rejected
                    'app_type': app_type,
                    'release_date': rdate
                }
            else:
                # Update release_date if already present
                final_results[unique_id]['release_date'] = rdate

        # Sort the queue by release date
        try:
            new_queue.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
        except ValueError:
            print("DEBUG: Invalid date format encountered during sorting.")
            pass

        # Update session variables
        session['decisions_queue_sorted'] = new_queue
        decisions_queue_sorted = new_queue
        session['final_results'] = final_results
    else:
        # Re-sort the existing queue by release date in case of any changes
        try:
            decisions_queue_sorted.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
            session['decisions_queue_sorted'] = decisions_queue_sorted
        except ValueError:
            print("DEBUG: Invalid date format encountered during re-sorting.")
            pass

    # Step 2: Define a Helper Function to Check if a Decision is Locked
    def is_locked(uid):
        locking_college = locked_until_opened.get(uid, None)
        return bool(locking_college and locking_college not in opened_colleges)

    # Step 3: Identify Available Decisions (Only the Earliest Unopened and Unlocked Decision)
    available_decisions = []
    for decision in decisions_queue_sorted:
        uid = decision['unique_id']
        if uid in opened_colleges:
            continue
        if is_locked(uid):
            continue
        available_decisions.append(uid)
        break  # Only the earliest available decision is clickable
    # Note: If you want multiple available decisions, adjust the loop accordingly

    # Step 4: Handle User Selecting a Decision to Open
    selected_college_id = request.args.get('selected_college')
    if selected_college_id and selected_college_id in available_decisions:
        if selected_college_id not in opened_colleges:
            opened_colleges.append(selected_college_id)
            session['opened_colleges'] = opened_colleges
        return redirect(url_for('results'))

    # Step 5: Build the List of Opened Decisions for Display
    opened_decisions_list = []
    for uid in opened_colleges:
        dq_item = next((x for x in decisions_queue_sorted if x['unique_id'] == uid), None)
        if not dq_item:
            continue

        short_name = dq_item['short_name']
        display_name = dq_item['display_name']
        app_type = dq_item['app_type']

        # Retrieve decision details from final_results
        info = final_results.get(uid, {})
        dcode = info.get('decision_code', 'R')
        date_str = info.get('release_date', '2099-01-01')

        # Map decision codes to display texts and badge classes
        decision_mapping = {
            "ED": ("ED Acceptance", "ed-acceptance"),
            "A": ("Acceptance", "acceptance"),
            "R": ("Rejection", "rejection"),
            "W": ("Waitlisted", "waitlist"),
            "D": ("Deferred", "deferred"),
            "D/R": ("Deferred Rejected", "deferred-rejection"),
            "D/A": ("Deferred Acceptance", "deferred-acceptance"),
            "D/W": ("Deferred Waitlist", "deferred-waitlist"),
        }
        display_decision, badge_class = decision_mapping.get(dcode, ("Unknown", "unknown"))

        formatted_dt = format_date(date_str)
        opened_decisions_list.append({
            "short_name": short_name,
            "display_name": display_name,
            "app_type": app_type,
            "decision": display_decision,
            "badge_class": badge_class,
            "release_date": formatted_dt
        })

    # Step 6: Schedule RD Decisions for Deferred Early Decisions
    for college in applied_colleges:
        short_name = college['short_name']
        app_type = college['app_type'].upper()
        early_unique_id = generate_unique_id(short_name, app_type)

        # Define deferred decision codes that warrant scheduling an RD
        deferred_codes = ['D', 'D/A', 'D/W', 'D/R']

        if final_results.get(early_unique_id, {}).get('decision_code') in deferred_codes:
            # Generate RD unique_id
            rd_unique_id = generate_unique_id(short_name, 'RD')

            # Check if RD decision is already scheduled
            rd_already_scheduled = (
                rd_unique_id in final_results or 
                any(d['unique_id'] == rd_unique_id for d in decisions_queue_sorted)
            )
            if not rd_already_scheduled:
                # Retrieve college entry
                c_entry_sim = next((c for c in college_list if c[0].lower() == short_name.lower()), None)
                if not c_entry_sim:
                    continue
                idx = college_list.index(c_entry_sim)

                # Determine RD release date
                if len(c_entry_sim) > 7 and c_entry_sim[7] != "N":
                    rd_release_date = c_entry_sim[7]
                else:
                    rd_release_date = "2099-01-01"

                # Retrieve university display info
                uni_info = next((uni for uni in university_list if uni["name"].lower() == short_name.lower()), None)
                if uni_info:
                    display_name = uni_info["display_name"]
                    logo_url = uni_info["logo"]
                else:
                    display_name = short_name.capitalize()
                    logo_url = "static/logos/default-logo.jpg"

                # Create RD decision entry
                rd_decision = {
                    "short_name": short_name.lower(),
                    "unique_id": rd_unique_id,
                    "display_name": display_name,
                    "app_type": "RD",
                    "release_date": rd_release_date,
                    "formatted_release_date": format_date(rd_release_date),
                    "logo_url": logo_url
                }

                # Append RD decision to the queue
                decisions_queue_sorted.append(rd_decision)

                # Initialize final_results for RD
                final_results[rd_unique_id] = {
                    'decision_code': 'PENDING',  # Placeholder status
                    'app_type': 'RD',
                    'release_date': rd_release_date
                }

                # Lock RD decision behind the early decision
                session.setdefault('locked_until_opened', {})
                session['locked_until_opened'][rd_unique_id] = early_unique_id

                print(f"DEBUG: Scheduled RD decision '{rd_unique_id}' for deferred early decision '{early_unique_id}'.")

    # Step 7: Update Session Variables After Scheduling RD Decisions
    session['decisions_queue_sorted'] = decisions_queue_sorted
    session['final_results'] = final_results

    # Step 8: Rebuild Visible Decisions After Scheduling RD
    visible_decisions = [
        decision for decision in decisions_queue_sorted 
        if decision['unique_id'] not in opened_colleges and not is_locked(decision['unique_id'])
    ]

    # Optional: Re-sort visible_decisions by release date
    try:
        visible_decisions.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
    except ValueError:
        print("DEBUG: Invalid date format encountered during final sorting of visible_decisions.")
        pass

    # Step 9: Render the Template with Updated Data
    return render_template(
        'results.html',
        name=name,
        decisions_queue=visible_decisions,  # Only visible (not opened or locked) decisions
        opened_decisions=opened_decisions_list,
        available_decisions=available_decisions,
        selected_college=selected_college_id
    )
    
def find_final_unique_id(college: str) -> str:
    final_results = session.get('final_results', {})
    # Collect all unique_ids that start with e.g. 'harvard_' or 'bing_'
    matching_uids = [uid for uid in final_results if uid.startswith(college.lower() + "_")]
    if not matching_uids:
        return None
    
    # If you create an RD record after deferral, it typically ends with "_rd"
    # Check if such an entry exists:
    rd_uids = [uid for uid in matching_uids if uid.endswith("_rd")]
    if rd_uids:
        # If there are multiple, pick the first or last—your choice. Usually there's just one.
        return rd_uids[-1]  # e.g., the last one in the list

    # Otherwise, pick the original ED/EA/REA unique_id (the first in matching_uids)
    return matching_uids[0]


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')  # e.g., December 19, 2024
    except ValueError:
        return "Unknown Date"

# Advanced Simulation Login Route
@app.route("/advancedsim/<college>/login", methods=["GET", "POST"])
def adv_login(college):
    user_data = session.get('advancedsim_data', {"name": "User"})
    unique_id = request.args.get('unique_id')  # e.g., 'northeastern_ed'
    if not unique_id:
        flash("No unique_id provided.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    decision_info = final_results.get(unique_id, {})
    release_date_str = decision_info.get('release_date', 'Unknown Date')
    name = user_data.get("name", "User")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Fake authentication check
        if not email or not password:
            return render_template(
                f"adv/{college}/login.html",
                error="Please fill out all fields.",
                college=college,
                name=name,
                release_date=release_date_str
            )
        
        # Check if the college is Northeastern
        if college.lower() == "northeastern":
            # Retrieve the decision_code from final_results
            decision_code = decision_info.get('decision_code', 'R')  # Default to 'R' if not found
            
            # Redirect based on the decision_code
            if decision_code in ["A", "ED", "D/A"]:
                return redirect(url_for("adv_acceptance", college=college, unique_id=unique_id))
            elif decision_code in ["D", "D/R"]:
                return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))
            elif decision_code in ["D/W"]:
                return redirect(url_for("adv_waitlist", college=college, unique_id=unique_id))
            elif decision_code == "W":
                return redirect(url_for("adv_waitlist", college=college, unique_id=unique_id))
            elif decision_code == "D/A":
                return redirect(url_for("adv_acceptance", college=college, unique_id=unique_id))
            else:
                # For any other or unknown decision_code, default to rejection
                return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))
        else:
            # For other colleges, proceed as usual to ustatus
            return redirect(url_for('adv_ustatus', college=college, unique_id=unique_id))

    # GET request: render the login page
    return render_template(
        f"adv/{college}/login.html",
        name=name,
        college=college,
        release_date=release_date_str
    )

@app.route("/advancedsim/<college>/ustatus", methods=["GET", "POST"])
@login_required
def adv_ustatus(college):
    from datetime import datetime
    user_data = session.get('advancedsim_data', {"name": "User", "date": "N/A"})
    final_results = session.get('final_results', {})

    # Retrieve unique_id from query parameters or form data
    unique_id = request.args.get('unique_id') or request.form.get('unique_id')
    if not unique_id:
        flash("Welcome back to your results page!", "info")
        return redirect(url_for('results'))

    info = final_results.get(unique_id)
    if not info:
        flash(f"No record found for {unique_id}.", "danger")
        return redirect(url_for('results'))

    decision_code = info.get('decision_code', 'R')
    release_date_str = info.get('release_date', 'Unknown Date')

    # Format the date
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    name = user_data.get("name", "User")

    if request.method == "POST":
        # Mark the college as opened
        if 'read_emails' not in session:
            session['read_emails'] = {}
        session['read_emails'][college.lower()] = True
        session.modified = True

        # Updated redirect logic
        if decision_code == "A":
            return redirect(url_for("adv_acceptance", college=college, unique_id=unique_id))
        elif decision_code == "ED":
            return redirect(url_for("adv_edacceptance", college=college, unique_id=unique_id))
        elif decision_code == "D":
            return redirect(url_for("adv_deferred", college=college, unique_id=unique_id))
        elif decision_code == "D/A":
            return redirect(url_for("adv_acceptance", college=college, unique_id=unique_id))
        elif decision_code == "D/R":
            return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))
        elif decision_code == "D/W":
            return redirect(url_for("adv_waitlist", college=college, unique_id=unique_id))
        elif decision_code == "W":
            return redirect(url_for("adv_waitlist", college=college, unique_id=unique_id))
        else:
            return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))

    # GET request: render status page
    return render_template(
        f"adv/{college}/ustatus.html",
        name=name,
        college=college,
        date=formatted_date,
        decision_code=decision_code,
        unique_id=unique_id  # Ensure unique_id is passed to the template
    )

@app.route("/advancedsim/<college>/acceptance")
@login_required
def adv_acceptance(college):
    unique_id = request.args.get('unique_id')
    if not unique_id:
        flash("No unique_id provided for acceptance letter.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    info = final_results.get(unique_id)
    if not info:
        flash("Acceptance record not found.", "danger")
        return redirect(url_for('results'))

    from datetime import datetime
    release_date_str = info.get('release_date', 'Unknown Date')
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    user_id = session.get('user_id')
    if user_id:
        User.log_simulation(user_id, college, 'acceptance')

    name = session.get("advancedsim_data", {}).get("name", "User")
    return render_template(
        f"adv/{college}/acceptance.html",
        name=name,
        date=formatted_date,
        college=college
    )

@app.route("/advancedsim/<college>/edacceptance")
@login_required
def adv_edacceptance(college):
    unique_id = request.args.get('unique_id')
    if not unique_id:
        flash("No unique_id provided for ED acceptance letter.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    info = final_results.get(unique_id)
    if not info:
        flash("ED acceptance record not found.", "danger")
        return redirect(url_for('results'))

    from datetime import datetime
    release_date_str = info.get('release_date', 'Unknown Date')
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    user_id = session.get('user_id')
    if user_id:
        User.log_simulation(user_id, college, 'edacceptance')

    name = session.get("advancedsim_data", {}).get("name", "User")
    return render_template(
        f"adv/{college}/edacceptance.html",
        name=name,
        date=formatted_date,
        college=college
    )

@app.route("/advancedsim/<college>/rejection")
@login_required
def adv_rejection(college):
    unique_id = request.args.get('unique_id')
    if not unique_id:
        flash("No unique_id provided for rejection letter.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    info = final_results.get(unique_id)
    if not info:
        flash("Rejection record not found.", "danger")
        return redirect(url_for('results'))

    from datetime import datetime
    release_date_str = info.get('release_date', 'Unknown Date')
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    user_id = session.get('user_id')
    if user_id:
        User.log_simulation(user_id, college, 'rejection')

    name = session.get("advancedsim_data", {}).get("name", "User")
    return render_template(
        f"adv/{college}/rejection.html",
        name=name,
        date=formatted_date,
        college=college
    )

@app.route("/advancedsim/<college>/deferred")
@login_required
def adv_deferred(college):
    unique_id = request.args.get('unique_id')
    if not unique_id:
        flash("No unique_id provided for deferred letter.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    info = final_results.get(unique_id)
    if not info:
        flash("Deferred record not found.", "danger")
        return redirect(url_for('results'))

    decision_code = info.get('decision_code', 'R')
    from datetime import datetime
    release_date_str = info.get('release_date', 'Unknown Date')
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    user_id = session.get('user_id')
    if user_id:
        # Only map 'D' to 'deferred'
        if decision_code == "D":
            User.log_simulation(user_id, college, 'deferred')
        else:
            # This route should not handle post-deferral outcomes
            User.log_simulation(user_id, college, 'deferred')  # Or handle differently

    name = session.get("advancedsim_data", {}).get("name", "User")
    return render_template(
        f"adv/{college}/deferred.html",
        name=name,
        date=formatted_date,
        college=college,
        decision_code=decision_code
    )

@app.route("/advancedsim/<college>/waitlist")
@login_required
def adv_waitlist(college):
    unique_id = request.args.get('unique_id')
    if not unique_id:
        flash("No unique_id provided for waitlist letter.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    info = final_results.get(unique_id)
    if not info:
        flash("Waitlist record not found.", "danger")
        return redirect(url_for('results'))

    from datetime import datetime
    release_date_str = info.get('release_date', 'Unknown Date')
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    user_id = session.get('user_id')
    if user_id:
        User.log_simulation(user_id, college, 'waitlist')

    name = session.get("advancedsim_data", {}).get("name", "User")
    return render_template(
        f"adv/{college}/waitlist.html",
        name=name,
        date=formatted_date,
        college=college
    )

@app.route('/advancedsim/results/mark_as_read', methods=["POST"])
@login_required
def mark_as_read():
    short_name = request.form.get('short_name')
    if not short_name:
        return {'status': 'fail', 'message': 'No short_name provided'}, 400
    if 'read_emails' not in session:
        session['read_emails'] = {}
    session['read_emails'][short_name.lower()] = True
    session.modified = True
    return {'status': 'success'}

@app.route('/quicksim/<college>/login_files/<path:filename>')
def login_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'login_files'), filename)

@app.route('/quicksim/<college>/ustatus_files/<path:filename>')
def ustatus_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'ustatus_files'), filename)

@app.route('/quicksim/<college>/acceptance_files/<path:filename>')
def acceptance_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'acceptance_files'), filename)

@app.route('/quicksim/<college>/deferred_files/<path:filename>')
def deferred_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'deferred_files'), filename)

@app.route('/quicksim/<college>/rejection_files/<path:filename>')
def rejection_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'rejection_files'), filename)

@app.route('/advancedsim_files/<path:filename>')
def advanced_files_static(filename):
    file_directory = os.path.join(app.root_path, 'templates', 'advancedsim_files')
    return send_from_directory(file_directory, filename)

@app.route('/advancedsim/<college>/login_files/<path:filename>')
def advancedsim_login_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'adv', college, 'login_files'), filename)

# Add similar routes for ustatus_files, acceptance_files, etc., if required:
@app.route('/advancedsim/<college>/ustatus_files/<path:filename>')
def advancedsim_ustatus_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'adv', college, 'ustatus_files'), filename)

@app.route('/advancedsim/<college>/acceptance_files/<path:filename>')
def advancedsim_acceptance_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'adv', college, 'acceptance_files'), filename)

@app.route('/advancedsim/<college>/rejection_files/<path:filename>')
def advancedsim_rejection_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'adv', college, 'rejection_files'), filename)

@app.route('/advancedsim/<college>/deferred_files/<path:filename>')
def advancedsim_deferred_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', 'adv', college, 'deferred_files'), filename)

if __name__ == "__main__":
    app.run(debug=True)
    