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
    "description": "Binghamton University, part of the State University of New York (SUNY) system, is a premier public institution known for its academic excellence and research opportunities. Located in Vestal, New York, Binghamton offers a diverse and vibrant campus community, rigorous academic programs, and a strong emphasis on affordability and student success."
    },
    {
        "name": "brown",
        "display_name": "Brown University",
        "logo": "static/logos/brown-logo.jpg",
        "description": "Brown University, founded in 1764 and located in Providence, Rhode Island, is an Ivy League institution known for its innovative Open Curriculum. Ranked consistently among the top 20 universities in the United States, Brown emphasizes interdisciplinary scholarship, undergraduate teaching, and a vibrant campus culture."
    },
    {
    "name": "buffalo",
    "display_name": "University at Buffalo",
    "logo": "static/logos/buffalo-logo.jpg",
    "description": "The University at Buffalo, part of the State University of New York (SUNY) system, is a leading public research university located in Buffalo, New York. Known for its diverse academic programs, robust research opportunities, and vibrant campus life, UB offers students an affordable yet world-class education. With a strong focus on innovation and community engagement, UB prepares students for success in a global society."
    },
    {
        "name": "caltech",
        "display_name": "California Institute of Technology",
        "logo": "static/logos/caltech-logo.jpg",
        "description": "The California Institute of Technology (Caltech), established in 1891 in Pasadena, California, is a small but prestigious science and engineering powerhouse. Frequently ranked among the world’s top 10 universities, Caltech is renowned for cutting-edge research in physics, astronomy, engineering, and the natural sciences."
    },
    {
        "name": "cmu",
        "display_name": "Carnegie Mellon University",
        "logo": "static/logos/cmu-logo.jpg",
        "description": "Carnegie Mellon University (CMU), founded in 1900 in Pittsburgh, Pennsylvania, is a global research university notable for top-ranked programs in computer science, fine arts, and engineering. CMU consistently ranks among the top 30 U.S. universities and is known for fostering a culture of innovation, entrepreneurship, and interdisciplinary exploration."
    },
    {
        "name": "columbia",
        "display_name": "Columbia University",
        "logo": "static/logos/columbia-logo.jpg",
        "description": "Columbia University, established in 1754 in the heart of New York City, is an Ivy League institution with a diverse range of undergraduate and graduate programs. Regularly ranked in the top 10 nationally, Columbia emphasizes a robust Core Curriculum, cutting-edge research, and close engagement with the cultural and professional opportunities of NYC."
    },
    {
        "name": "cornell",
        "display_name": "Cornell University",
        "logo": "static/logos/cornell-logo.jpg",
        "description": "Cornell University, founded in 1865 in Ithaca, New York, is both an Ivy League and land-grant institution. It offers a wide array of programs across its undergraduate colleges and professional schools. Routinely ranked among the top 20 universities, Cornell is celebrated for its commitment to public engagement, interdisciplinary research, and inclusive community."
    },
    {
        "name": "dartmouth",
        "display_name": "Dartmouth College",
        "logo": "static/logos/dartmouth-logo.png",
        "description": "Dartmouth College, established in 1769 in Hanover, New Hampshire, is an Ivy League institution emphasizing a liberal arts undergraduate education. Regularly placed in the top 15 U.S. colleges, Dartmouth provides a close-knit community, small class sizes, and a distinctive focus on experiential learning and undergraduate research."
    },
    {
        "name": "duke",
        "display_name": "Duke University",
        "logo": "static/logos/duke-logo.jpg",
        "description": "Duke University, founded in 1838 in Durham, North Carolina, is a private research university known for strong programs in medicine, engineering, public policy, and the liberal arts. Often ranked in the top 10-15 nationally, Duke combines rigorous academics with a spirited athletic culture and a global outlook."
    },
    {
        "name": "gtech",
        "display_name": "Georgia Tech",
        "logo": "static/logos/gtech-logo.jpg",
        "description": "The Georgia Institute of Technology, founded in 1885 in Atlanta, Georgia, is a leading public research university. Known for top-tier engineering, computing, and business programs, Georgia Tech ranks among the top 10 public universities in the U.S. and fosters a culture of innovation and applied research."
    },
    {
        "name": "harvard",
        "display_name": "Harvard University",
        "logo": "static/logos/harvard-logo.jpg",
        "description": "Harvard University, established in 1636 in Cambridge, Massachusetts, is the oldest institution of higher learning in the U.S. Consistently ranked #1 or #2 globally, Harvard offers unparalleled resources, a vast network of alumni, and a broad range of top-ranked programs in the arts, sciences, medicine, law, and business."
    },
    {
        "name": "jhu",
        "display_name": "Johns Hopkins University",
        "logo": "static/logos/jhu-logo.jpg",
        "description": "Johns Hopkins University, founded in 1876 in Baltimore, Maryland, pioneered the modern research university model in the U.S. Renowned for its medical school, public health, international studies, and biomedical engineering programs, JHU consistently ranks in the top 15 nationally and is a global leader in groundbreaking research."
    },
    {
        "name": "mit",
        "display_name": "Massachusetts Institute of Technology",
        "logo": "static/logos/mit-logo.jpg",
        "description": "The Massachusetts Institute of Technology (MIT), established in 1861 in Cambridge, Massachusetts, is a world leader in science, technology, and engineering education. Perennially ranked among the top 5 universities worldwide, MIT is known for a culture of invention, interdisciplinary collaboration, and hands-on problem-solving."
    },
    {
        "name": "northwestern",
        "display_name": "Northwestern University",
        "logo": "static/logos/northwestern-logo.jpg",
        "description": "Northwestern University, founded in 1851 in Evanston, Illinois (just north of Chicago), is a top-10 U.S. research university. Renowned for its journalism, business (Kellogg), law, and performing arts programs, Northwestern champions interdisciplinary collaborations and provides students with rich academic and cultural opportunities."
    },
    {
        "name": "nyu",
        "display_name": "New York University",
        "logo": "static/logos/nyu-logo.jpg",
        "description": "New York University (NYU), established in 1831, is located in the heart of Manhattan. With global campuses and a wide array of programs, NYU is recognized for its business, film, performing arts, and social science disciplines. Routinely ranked in the top 30 U.S. universities, NYU offers unparalleled internship and cultural experiences."
    },
    {
        "name": "princeton",
        "display_name": "Princeton University",
        "logo": "static/logos/princeton-logo.jpg",
        "description": "Princeton University, founded in 1746 in Princeton, New Jersey, is one of the world’s foremost Ivy League institutions. Consistently ranked #1 or #2 among U.S. universities, Princeton is celebrated for its rigorous undergraduate focus, generous financial aid, and research excellence across the humanities, sciences, and engineering."
    },
    {
    "name": "rice",
    "display_name": "Rice University",
    "logo": "static/logos/rice-logo.jpg",
    "description": "Founded in 1912 in Houston, Texas, Rice University is a leading research institution known for its distinctive residential college system, close-knit campus community, and interdisciplinary approach to education. Consistently ranked among the nation’s top universities, Rice boasts a strong emphasis on undergraduate teaching, world-class STEM programs, and a tradition of fostering collaboration, innovation, and scholarly excellence."
    },
    {
        "name": "stanford",
        "display_name": "Stanford University",
        "logo": "static/logos/stanford-logo.jpg",
        "description": "Stanford University, established in 1885 near Palo Alto, California, is a top-tier private research institution known for its entrepreneurial spirit and proximity to Silicon Valley. Frequently ranked among the world’s top 5 universities, Stanford excels in engineering, business, computer science, the humanities, and the sciences."
    },
    {
        "name": "berkeley",
        "display_name": "University of California, Berkeley",
        "logo": "static/logos/berkeley-logo.png",
        "description": "The University of California, Berkeley, founded in 1868 in the San Francisco Bay Area, is the flagship campus of the UC system. Consistently ranked the #1 public university in the U.S., Berkeley leads in sciences, engineering, social sciences, and the humanities, with a renowned tradition of public service and political activism."
    },
    {
        "name": "umich",
        "display_name": "University of Michigan",
        "logo": "static/logos/umich-logo.png",
        "description": "The University of Michigan, established in 1817 in Ann Arbor, is a top public research university noted for its outstanding faculty, diverse academic programs, and passionate athletic community. Consistently ranked in the top 25, UMich excels across disciplines, from engineering and medicine to business, arts, and the social sciences."
    },
    {
        "name": "uchicago",
        "display_name": "University of Chicago",
        "logo": "static/logos/uchicago-logo.jpg",
        "description": "The University of Chicago, founded in 1890 on the South Side of Chicago, is world-renowned for its rigorous intellectual environment, the Core Curriculum, and strengths in economics, law, and the social sciences. Regularly in the top 10, UChicago’s culture of inquiry fosters transformative research and critical debate."
    },
    {
        "name": "upenn",
        "display_name": "University of Pennsylvania",
        "logo": "static/logos/upenn-logo.jpg",
        "description": "The University of Pennsylvania (Penn), established in 1740 in Philadelphia, is an Ivy League university that blends liberal arts and professional education. Consistently ranked in the top 10, Penn is celebrated for the Wharton School of Business, as well as top programs in law, medicine, and the social sciences."
    },
    {
        "name": "usc",
        "display_name": "University of Southern California",
        "logo": "static/logos/usc-logo.png",
        "description": "The University of Southern California (USC), founded in 1880 in Los Angeles, is a leading private research institution. Known for its world-class film school, strong engineering, business, and communication programs, USC offers a vibrant campus life, global outreach, and deep connections to the industries of Southern California."
    },
    {
        "name": "yale",
        "display_name": "Yale University",
        "logo": "static/logos/yale-logo.jpg",
        "description": "Yale University, established in 1701 in New Haven, Connecticut, is an Ivy League institution renowned for its stellar liberal arts education, top-ranked law school, and vibrant arts programs. Consistently placed among the top 3-5 U.S. universities, Yale’s residential college system, world-class faculty, and global network ensure a transformative academic experience."
    }
]

college_list = [
    ["columbia", "0.02", "1.9", "N", "P", "2024-12-18", "N", "2025-03-28"],
    ["stanford", "0.03", "N", "1.3", "REA", "2024-12-13", "N", "2025-03-29"],
    ["upenn", "0.03", "2.3", "N", "P", "2024-12-18", "N", "2025-03-28"],
    ["caltech", "0.03", "N", "1.1", "REA", "2024-12-12", "N", "2025-03-25"],
    ["jhu", "0.05", "1.7", "N", "P", "2024-12-13", "N", "2025-03-21"],
    ["dartmouth", "0.05", "2.3", "N", "P", "2024-12-13", "N", "2025-03-28"],
    ["princeton", "0.06", "N", "1.3", "REA", "2024-12-12", "N", "2025-03-28"],
    ["mit", "0.06", "N", "1.2", "P", "N", "2024-12-17", "2025-03-14"],
    ["yale", "0.07", "N", "1.3", "REA", "2024-12-17", "N", "2025-03-28"],
    ["harvard", "0.07", "N", "1.3", "REA", "2024-12-12", "N", "2025-03-28"],
    ["brown", "0.08", "2.0", "N", "P", "2024-12-13", "N", "2025-03-28"],
    ["uchicago", "0.09", "2.5", "1.3", "P", "2024-12-20", "2024-12-20", "2025-03-25"],
    ["northwestern", "0.09", "2.2", "N", "P", "2024-12-17", "N", "2025-03-24"],
    ["duke", "0.10", "2.0", "N", "P", "2024-12-16", "N", "2025-03-28"],
    ["rice", "0.12", "2", "N", "P", "2024-12-14", "N", "2025-03-21"],
    ["cornell", "0.15", "2.2", "N", "P", "2024-12-12", "N", "2025-03-28"],
    ["gtech", "0.15", "N", "1.4", "PUB", "N", "2025-1-27", "2025-03-28"],
    ["berkeley", "0.15", "N", "N", "PUB", "N", "N", "2025-03-27"],
    ["usc", "0.17", "N", "1.3", "P", "N", "2025-1-17", "2025-03-16"],
    ["umich", "0.2", "N", "1.3", "PUB", "N", "2025-1-27", "2025-03-10"],
    ["nyu", "0.22", "1.5", "N", "P", "2024-12-12", "N", "2025-04-01"],
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
        acceptances = len([sim for sim in uni_simulations if sim['result'] == 'acceptance'])
        rejections = len([sim for sim in uni_simulations if sim['result'] == 'rejection'])
        success_rate = (acceptances / total) * 100 if total > 0 else 0
        stats[uni_name] = {
            'display_name': uni['display_name'],
            'logo': uni['logo'],
            'description': uni['description'],  # Pass description directly
            'total_simulations': total,
            'acceptances': acceptances,
            'rejections': rejections,
            'success_rate': round(success_rate, 2)
        }

    # Sort by acceptances and rejections
    sorted_by_acceptances = sorted(stats.values(), key=lambda x: x['acceptances'], reverse=True)[:5]
    sorted_by_rejections = sorted(stats.values(), key=lambda x: x['rejections'], reverse=True)[:5]

    return render_template(
        'statistics.html',
        acceptances_stats=sorted_by_acceptances,
        rejections_stats=sorted_by_rejections,
        sorted_stats=sorted(stats.values(), key=lambda x: x['total_simulations'], reverse=True)
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
    return render_template(f"{college}/ustatus.html", name=user_data["name"], date=user_data["date"], college=college)

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

@app.route('/advancedsim/summary')
@login_required
def summary():
    # Retrieve User Profile Data from session['advancedsim_data']
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

    # Gather Applied Colleges with Application Types
    applied_colleges = []

    # Early Decision (ED)
    ed_school = session.get('ed_school')
    if ed_school:
        college_entry = next((col for col in college_list if col[0].lower() == ed_school.lower()), None)
        university_info = next((uni for uni in university_list if uni["name"].lower() == ed_school.lower()), None)
        if college_entry and university_info:
            applied_colleges.append({
                "app_type": "ED",
                "short_name": college_entry[0].lower(),
                "display_name": university_info["display_name"],
                "logo_url": university_info["logo"],
                "public": "Public" if college_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Restrictive Early Action (REA)
    rea_school = session.get('rea_school')
    if rea_school:
        college_entry = next((col for col in college_list if col[0].lower() == rea_school.lower()), None)
        university_info = next((uni for uni in university_list if uni["name"].lower() == rea_school.lower()), None)
        if college_entry and university_info:
            applied_colleges.append({
                "app_type": "REA",
                "short_name": college_entry[0].lower(),
                "display_name": university_info["display_name"],
                "logo_url": university_info["logo"],
                "public": "Public" if college_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Early Action (EA)
    ea_schools = session.get('ea_schools', [])
    for ea_school in ea_schools:
        college_entry = next((col for col in college_list if col[0].lower() == ea_school.lower()), None)
        university_info = next((uni for uni in university_list if uni["name"].lower() == ea_school.lower()), None)
        if college_entry and university_info:
            applied_colleges.append({
                "app_type": "EA",
                "short_name": college_entry[0].lower(),
                "display_name": university_info["display_name"],
                "logo_url": university_info["logo"],
                "public": "Public" if college_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Regular Decision (RD)
    rd_schools = session.get('rd_schools', [])
    for rd_school in rd_schools:
        college_entry = next((col for col in college_list if col[0].lower() == rd_school.lower()), None)
        university_info = next((uni for uni in university_list if uni["name"].lower() == rd_school.lower()), None)
        if college_entry and university_info:
            applied_colleges.append({
                "app_type": "RD",
                "short_name": college_entry[0].lower(),
                "display_name": university_info["display_name"],
                "logo_url": university_info["logo"],
                "public": "Public" if college_entry[4].upper() in ["PUB", "P"] else "Private"
            })

    # Sort Applied Colleges by Application Type Order (ED, REA, EA, RD)
    type_order = {"ED": 1, "REA": 2, "EA": 3, "RD": 4}
    applied_colleges.sort(key=lambda x: type_order.get(x["app_type"], 5))

    # Store `applied_colleges` in the session
    session['applied_colleges'] = applied_colleges

    print("Summary Route - Applied Colleges:", applied_colleges)  # Debugging

    # Build decisions_queue with necessary information
    decisions_queue = []
    for college in applied_colleges:
        short_name = college.get('short_name', '').lower()
        display_name = college.get('display_name', 'Unknown')
        app_type = college.get('app_type', 'Unknown').upper() 
        logo_url = college.get('logo_url', 'static/logos/default-logo.jpg')  # Default logo if missing

        # Fetch release_date based on app_type from college_list
        c_entry = next((c for c in college_list if c[0].lower() == short_name), None)
        if not c_entry:
            print(f"College '{short_name}' not found in college_list. Skipping.")
            continue

        # Determine release date based on application type
        if app_type == "ED":
            release_date_str = c_entry[5] if c_entry[5] != "N"  else "2099-01-01"
        elif app_type == "REA":
            release_date_str = c_entry[5] if c_entry[5] != "N" else "2099-01-01"
        elif app_type == "EA":
            release_date_str = c_entry[6] if c_entry[6] != "N" else "2099-01-01"
        else:  # RD or Deferred
            release_date_str = c_entry[7] if c_entry[7] != "N" else "2099-01-01"

        # Append to decisions_queue
        unique_id = f"{short_name}_{app_type}".lower()
        decisions_queue.append({
            "short_name": short_name,
            "unique_id": unique_id,  # Ensure unique_id is set
            "display_name": display_name,
            "app_type": app_type,
            "release_date": release_date_str,
            "formatted_release_date": format_date(release_date_str),
            "logo_url": logo_url
        })

    # Sort decisions_queue by release_date
    try:
        decisions_queue_sorted = sorted(
            decisions_queue,
            key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d')
        )
    except ValueError as e:
        print(f"Error sorting decisions: {e}")
        decisions_queue_sorted = decisions_queue  # Fallback to unsorted if error

    print("Decisions Queue Sorted:", decisions_queue_sorted)  # Debugging

    # Update final_results with release_date
    final_results = session.get('final_results', {})
    
    for decision in decisions_queue_sorted:
        short_name = decision.get('short_name')
        app_type = decision.get('app_type').upper()
        release_date_str = decision.get('release_date')

        unique_id = f"{short_name}_{app_type}".lower()

        if unique_id not in final_results:
            final_results[unique_id] = {
                'decision_code': 'R',  # Default to Rejected
                'app_type': app_type,
                'release_date': release_date_str
            }

    session['final_results'] = final_results

    # Format release dates for better readability
    for decision in decisions_queue_sorted:
        try:
            date_obj = datetime.strptime(decision['release_date'], '%Y-%m-%d')
            decision['formatted_release_date'] = date_obj.strftime('%B %d, %Y')  # e.g., December 19, 2024
        except ValueError:
            decision['formatted_release_date'] = "Unknown Date"

    print("Decisions Queue Sorted with Formatted Dates:", decisions_queue_sorted)  # Debugging

    # Pass to template
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
        return "Highly Likely", "highly-likely"
    elif chance > 65:
        return "Safety", "safety"
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
    if student_num >= 96:
        return 1
    elif student_num >= 91:
        return 2
    elif student_num >= 83:
        return 3
    elif student_num >= 75:
        return 4
    elif student_num >= 70:
        return 5
    elif student_num >= 67:
        return 6
    elif student_num >= 58:
        return 7
    elif student_num >= 51:
        return 8
    elif student_num >= 40:
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
        student_num += interviewScore * 1.5
        student_num += essayStrength * 1.5
        student_num -= 4
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
        student_num += ap_courses * 1
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
            chances = 75 + random.uniform(-5, 5)
        elif tier == 2:
            chances = 67 + random.uniform(-4, 2)
        elif tier == 3:
            chances = 62 + random.uniform(-4, 2)
        elif tier == 4:
            chances = 55 + random.uniform(-4, 2)
        elif tier == 5:
            chances = 44 + random.uniform(-4, 2)
        elif tier == 6:
            chances = 37 + random.uniform(-4, 2)
        elif tier == 7:
            chances = 33 + random.uniform(-4, 2)
        elif tier == 8:
            chances = 25 + random.uniform(-4, 2)
        elif tier == 9:
            chances = 18 + random.uniform(-4, 2)
        elif tier == 10:
            chances = 12 + random.uniform(-4, 2)
        else:
            chances = 4 + random.uniform(-0.1, 0.1) - 2
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

    chances -= random.uniform(-1, 3)  # Simulating chances -= Math.random()*4 -1

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

# Chances Route
@app.route('/advancedsim/chances', methods=["GET", "POST"])
@login_required
def chances():
    # Clear previous simulation state
    session.pop('read_emails', None)
    session.pop('current_sim_date', None)
    session.pop('simulation_started', None)
    session.pop('final_results', None)
    session.pop('deferred_decisions', None)  # If you have deferred decisions
    session.pop('opened_colleges', None)     # Clear opened_colleges as well
    session.pop('decisions_queue_sorted', None)  # Clear decisions_queue_sorted

    if request.method == 'POST':
        # After reviewing chances, proceed to results page
        flash("Chances reviewed successfully!", "success")
        # Generate final decisions and store them
        user_data = session.get('advancedsim_data', {})
        applied_colleges = session.get('applied_colleges', [])
        interview_chances = session.get('interview_chances', {})

        final_results = session.get('final_results', {})  # Get existing final_results
        decisions_queue_sorted = session.get('decisions_queue_sorted', [])

        # Build decisions_queue_sorted if not already
        if not decisions_queue_sorted:
            # Build decisions_queue_sorted similar to /results route
            decisions_queue_sorted = []
            for college in applied_colleges:
                short_name = college.get('short_name', '').lower()
                display_name = college.get('display_name', 'Unknown')
                app_type = college.get('app_type', 'Unknown').upper() 
                logo_url = college.get('logo_url', 'static/logos/default-logo.jpg')  # Default logo if missing

                # Fetch release_date based on app_type from college_list
                c_entry = next((c for c in college_list if c[0].lower() == short_name), None)
                if not c_entry:
                    print(f"College '{short_name}' not found in college_list. Skipping.")
                    continue

                # Determine release date based on application type
                if app_type == "ED":
                    release_date_str = c_entry[5] if len(c_entry) > 5 and c_entry[5] != "N" else "2099-01-01"
                elif app_type == "REA":
                    release_date_str = c_entry[5] if len(c_entry) > 5 and c_entry[5] != "N" else "2099-01-01"
                elif app_type == "EA":
                    release_date_str = c_entry[6] if len(c_entry) > 6 and c_entry[6] != "N" else "2099-01-01"
                else:  # RD
                    release_date_str = c_entry[7] if len(c_entry) > 7 and c_entry[7] != "N" else "2099-01-01"

                unique_id = f"{short_name}_{app_type}".lower()
                # Append to decisions_queue_sorted
                decisions_queue_sorted.append({
                    "short_name": short_name,
                    "unique_id": unique_id,  # Ensure unique_id is set
                    "display_name": display_name,
                    "app_type": app_type,
                    "release_date": release_date_str,
                    "formatted_release_date": format_date(release_date_str),
                    "logo_url": logo_url
                })

                # Update final_results with release_date if not already present using unique_id
                if unique_id not in final_results:
                    final_results[unique_id] = {
                        'decision_code': 'R',  # Default to Rejected
                        'app_type': app_type,
                        'release_date': release_date_str
                    }

            # Sort decisions_queue_sorted by release_date
            try:
                decisions_queue_sorted = sorted(
                    decisions_queue_sorted,
                    key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d')
                )
            except ValueError as e:
                print(f"Error sorting decisions: {e}")
                # Fallback to unsorted

        # Process each interview chance and determine decision
        for unique_id, data in interview_chances.items():
            # unique_id is already in the format 'short_name_app_type'
            try:
                college_short_name, app_type = unique_id.split('_', 1)
                app_type = app_type.upper()
            except ValueError:
                print(f"Invalid unique_id format: {unique_id}")
                continue

            college_entry = next((c for c in college_list if c[0].lower() == college_short_name.lower()), None)
            if not college_entry:
                print(f"College entry not found for short_name: {college_short_name}")
                continue
            chances_val = data['chances']
            idx = college_list.index(college_entry)
            # Get final decision
            decision_code = admissionsDecision(
                chances_val,
                app_type,
                idx,
                college_list,
                decisions_queue_sorted
            )

            # Update final_results using unique_id
            final_results[unique_id] = {
                'decision_code': decision_code,
                'app_type': app_type,
                'release_date': college_entry[7] if len(college_entry) > 7 else '2099-01-01'
            }

        # Update session['final_results'] with the merged data
        session['final_results'] = final_results
        session['decisions_queue_sorted'] = decisions_queue_sorted  # Save sorted queue to session
        session.pop('opened_colleges', None)      # Ensure opened_colleges is cleared

        return redirect(url_for('results'))

    # Handle GET request
    user_data = session.get('advancedsim_data', {})
    applied_colleges = session.get('applied_colleges', [])
    if not applied_colleges:
        flash("No applied colleges found.", "warning")
        return redirect(url_for('summary'))

    # Extract user data
    demScore = user_data.get('dem_score', 0.0)
    testOption = user_data.get('test_option', 'rd').lower()
    testOptional = (testOption == 'optional')
    sat = user_data.get('sat_score', -1)
    try:
        sat = int(sat) if sat is not None else -1
    except:
        sat = -1
    act = user_data.get('act_score', -1)
    try:
        act = int(act) if act is not None else -1
    except:
        act = -1
    extracurriculars = user_data.get('extracurriculars', 0)
    ap_courses = user_data.get('ap_courses', 0)
    essayStrength = user_data.get('essays', 0)
    gpa = user_data.get('gpa', 0.0)

    interview_chances = {}
    for college in applied_colleges:
        display_name = college['display_name']
        app_type = college['app_type'].upper()  # Ensure app_type is uppercase
        short_name = college.get('short_name', '').lower()
        university_info = next((uni for uni in university_list if uni['name'].lower() == short_name), None)
        if not university_info:
            print(f"University info not found for short_name: {short_name}")
            continue
        college_entry = next((c for c in college_list if c[0].lower() == short_name), None)
        if not college_entry:
            print(f"College entry not found for short_name: {short_name}")
            continue
        i = college_list.index(college_entry)
        interview_score = sim10()
        chances_value = chanceCollege(
            collegeList=college_list,
            i=i,
            demScore=demScore,
            testOptional=testOptional,
            sat=sat,
            act=act,
            extracurriculars=extracurriculars,
            ap_courses=ap_courses,
            essayStrength=essayStrength,
            gpa=gpa,
            interviewStrength=interview_score,
            app_type=app_type
        )
        chance_category, chance_class = getType(chances_value)
        rate_label, rate_class = rate(interview_score)
        public_status = college_entry[4]
        public_status = "Public" if public_status.upper() in ["PUB", "P"] else "Private"

        unique_id = f"{short_name}_{app_type}".lower()

        interview_chances[unique_id] = {  # Use unique_id as key
            "display_name": display_name,
            "interview_score": interview_score,
            "interview_rate_label": rate_label,
            "interview_rate_class": rate_class,
            "chances": chances_value,
            "chance_category": chance_category,
            "chance_class": chance_class,
            "app_type": app_type,
            "public": public_status,
            "logo_url": university_info["logo"]
        }

    session['interview_chances'] = interview_chances

    print("Chances Route - Interview Chances:", interview_chances)  # Debugging

    return render_template('chances.html', interview_chances=interview_chances)

# see if u get accepted or no
# Admissions Decision Function
def admissionsDecision(chances, appType, idx, college_list, decisions_queue_sorted, is_deferred=False):
    yourFate = min(random.random() * 100, random.random() * 100) + random.random() * 30
    collegeName = college_list[idx][0].lower()

    print(f"Admissions Decision for {collegeName}:")
    print(f"App Type: {appType}, Chances: {chances}, Fate: {yourFate}")

    if appType == "ED":
        if yourFate < chances:
            decision = "A"    # Admitted
        elif yourFate < chances + random.random() * 30:
            decision = "D"    # Deferred
        else:
            decision = "R"    # Rejected
    elif appType == "REA":
        if yourFate < chances:
            decision = "A"
        elif yourFate < chances + random.random() * 25:
            decision = "D"
        else:
            decision = "R"
    elif appType == "EA":
        if yourFate < chances:
            decision = "A"
        elif yourFate < chances + random.random() * 40:
            decision = "D"
        else:
            decision = "R"
    elif appType == "RD":
        if yourFate < chances:
            decision = "A"
        elif yourFate < chances + random.random() * 15:
            decision = "W"  # Waitlisted
        else:
            decision = "R"
    else:
        decision = "NO"
        print(f"Unknown application type: {appType}")

    # Handle Deferred Decision
    if decision == "D" and not is_deferred:
        # Append the deferred decision as a combined decision
        secondary_decision_code = determine_secondary_decision(chances)
        combined_decision = f"D/{secondary_decision_code}"
        print(f"Combined Deferred Decision: {combined_decision}")
        decision = combined_decision

        # Update final_results with combined decision
        unique_id = f"{collegeName}_{appType}".lower()
        if 'final_results' not in session:
            session['final_results'] = {}
        session['final_results'][unique_id]['decision_code'] = decision
        session.modified = True

    # Create unique_id
    unique_id = f"{collegeName}_{appType}".lower()

    if 'final_results' not in session:
        session['final_results'] = {}
    session['final_results'][unique_id] = {
        'decision_code': decision,
        'app_type': appType,
        'release_date': college_list[idx][7] if len(college_list[idx]) > 7 else '2099-01-01'
    }

    print(f"Decision: {decision}")

    return decision

def determine_secondary_decision(chances):
    modified_chances = chances + (random.random() * 20) - 10
    modified_chances = max(0.0, min(modified_chances, 100.0))  # Ensure within 0-100%

    print(f"Secondary Decision: Original Chances: {chances}, Modified Chances: {modified_chances}")

    yourFate = random.uniform(0, 100)
    if yourFate < modified_chances:
        secondary_decision = "A"  # Admitted
    elif yourFate < modified_chances + random.uniform(0, 15):
        secondary_decision = "W"  # Waitlisted
    else:
        secondary_decision = "R"  # Rejected

    return secondary_decision

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

# Results Route
@app.route('/advancedsim/results', methods=["GET", "POST"])
@login_required
def results():
    # Retrieve user profile data from session
    user_data = session.get('advancedsim_data', {"name": "User"})
    name = user_data.get("name", "User")

    # Retrieve applied colleges and final results from session
    applied_colleges = session.get('applied_colleges', [])
    final_results = session.get('final_results', {})
    read_emails = session.get('read_emails', {})

    # Retrieve opened_colleges from session or initialize
    opened_colleges = session.get('opened_colleges', [])

    # Retrieve decisions_queue_sorted from session or build it
    decisions_queue_sorted = session.get('decisions_queue_sorted', [])

    if not decisions_queue_sorted:
        # Build decisions_queue_sorted from applied_colleges if not in session
        decisions_queue_sorted = []
        for college in applied_colleges:
            short_name = college.get('short_name', '').lower()
            display_name = college.get('display_name', 'Unknown')
            app_type = college.get('app_type', 'Unknown').upper() 
            logo_url = college.get('logo_url', 'static/logos/default-logo.jpg')  # Default logo if missing

            # Fetch release_date based on app_type from college_list
            c_entry = next((c for c in college_list if c[0].lower() == short_name), None)
            if not c_entry:
                print(f"College '{short_name}' not found in college_list. Skipping.")
                continue

            # Determine release date based on application type
            if app_type == "ED":
                release_date_str = c_entry[5] if len(c_entry) > 5 and c_entry[5] != "N" else "2099-01-01"
            elif app_type == "REA":
                release_date_str = c_entry[5] if len(c_entry) > 5 and c_entry[5] != "N" else "2099-01-01"
            elif app_type == "EA":
                release_date_str = c_entry[6] if len(c_entry) > 6 and c_entry[6] != "N" else "2099-01-01"
            else:  # RD
                release_date_str = c_entry[7] if len(c_entry) > 7 and c_entry[7] != "N" else "2099-01-01"

            # Append to decisions_queue_sorted
            unique_id = f"{short_name}_{app_type}".lower()
            decisions_queue_sorted.append({
                "short_name": short_name,
                "unique_id": unique_id,  # Ensure unique_id is set
                "display_name": display_name,
                "app_type": app_type,
                "release_date": release_date_str,
                "formatted_release_date": format_date(release_date_str),
                "logo_url": logo_url
            })

            # Update final_results with release_date if not already present using unique_id
            if unique_id not in final_results:
                final_results[unique_id] = {
                    'decision_code': 'R',  # Default to Rejected
                    'app_type': app_type,
                    'release_date': release_date_str
                }

        # Sort decisions_queue_sorted by release_date
        try:
            decisions_queue_sorted = sorted(
                decisions_queue_sorted,
                key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d')
            )
        except ValueError as e:
            print(f"Error sorting decisions: {e}")
            # Fallback to unsorted

        print("Decisions Queue Sorted (built):", decisions_queue_sorted)  # Debugging

        # Save to session
        session['decisions_queue_sorted'] = decisions_queue_sorted
        session['final_results'] = final_results

    else:
        # If 'decisions_queue_sorted' exists, ensure it's sorted
        try:
            decisions_queue_sorted = sorted(
                decisions_queue_sorted,
                key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d')
            )
            session['decisions_queue_sorted'] = decisions_queue_sorted
        except ValueError as e:
            print(f"Error sorting decisions from session: {e}")
            # Fallback to unsorted

        print("Decisions Queue Sorted (from session):", decisions_queue_sorted)  # Debugging

    # Initialize app_type with a default value to prevent UnboundLocalError
    app_type = "Unknown"

    # Determine the first unopened status update
    first_unopened = None
    for decision in decisions_queue_sorted:
        # Debugging: Check if 'unique_id' exists
        if 'unique_id' not in decision:
            print(f"Decision entry missing 'unique_id': {decision}")
            continue  # Skip entries without 'unique_id'

        if decision['unique_id'] not in opened_colleges:
            first_unopened = decision['unique_id']
            break

    # Handle 'selected_college' query parameter
    selected_college_unique_id = request.args.get('selected_college', None)
    if selected_college_unique_id:
        # Split unique_id into short_name and app_type
        try:
            selected_short_name, selected_app_type = selected_college_unique_id.split('_', 1)
        except ValueError:
            selected_short_name = selected_college_unique_id
            selected_app_type = 'Unknown'

        selected_unique_id = selected_college_unique_id.lower()

        # Ensure app_type is uppercase before processing
        selected_app_type = selected_app_type.upper()

        # Check if unique_id is already in opened_colleges
        if selected_unique_id not in opened_colleges:
            # Add to opened_colleges
            opened_colleges.append(selected_unique_id)
            session['opened_colleges'] = opened_colleges

            # Get the decision_code to determine if deferred
            decision_info = final_results.get(selected_unique_id, {})
            decision_code = decision_info.get('decision_code', 'R')

            if decision_code.startswith("D/"):
                # Already a combined deferred decision; no further action
                pass
            elif decision_code == "D":
                # Handle scheduling if necessary
                # But with combined decisions, this may not be needed
                pass

            # After opening, automatically set the next status update as active
            remaining_decisions = [
                d['unique_id'] for d in decisions_queue_sorted if d['unique_id'] not in opened_colleges
            ]
            if remaining_decisions:
                next_selected_unique_id = remaining_decisions[0]
                selected_college_unique_id = next_selected_unique_id
                # Do not add to opened_colleges yet; wait until clicked
            else:
                selected_college_unique_id = None
    else:
        # If no selected_college is provided, set it to the first unopened decision
        selected_college_unique_id = first_unopened

    # Collect all opened decisions to display in main content
    opened_decisions = []
    for unique_id in opened_colleges:
        # Split unique_id to get short_name and app_type
        try:
            short_name, app_type = unique_id.split('_', 1)
        except ValueError:
            short_name = unique_id
            app_type = 'Unknown'

        decision_info = final_results.get(unique_id, {})
        decision_code = decision_info.get('decision_code', 'R')  # Default to 'R' (Rejected)
        app_type = decision_info.get('app_type', 'Unknown').upper()
        release_date_str = decision_info.get('release_date', 'Unknown Date')

        # Format release date
        formatted_release_date = format_date(release_date_str)

        # Map decision_code to display info and badge class
        if decision_code == "A":
            display_decision = "Acceptance"
            badge_class = "acceptance"
        elif decision_code == "E":
            display_decision = "Early Decision Acceptance"
            badge_class = "acceptance"
        elif decision_code.startswith("D/"):
            # Combined Deferred Decision
            secondary_decision = decision_code.split('/')[1]
            if secondary_decision == "A":
                display_decision = "Deferred Acceptance"
                badge_class = "acceptance"
            elif secondary_decision == "W":
                display_decision = "Deferred Waitlist"
                badge_class = "waitlist"
            elif secondary_decision == "R":
                display_decision = "Deferred Rejection"
                badge_class = "rejection"
            else:
                display_decision = "Deferred Unknown"
                badge_class = "unknown"
        elif decision_code == "D":
            display_decision = "Deferred"
            badge_class = "deferred"
        elif decision_code == "W":
            display_decision = "Waitlisted"
            badge_class = "waitlist"
        elif decision_code == "R":
            display_decision = "Rejection"
            badge_class = "rejection"
        else:
            display_decision = "Unknown"
            badge_class = "unknown"

        # Get display name
        display_name = next(
            (uni["display_name"] for uni in university_list if uni["name"].lower() == short_name),
            short_name.capitalize()
        )

        # Get logo_url
        logo_url = next(
            (uni["logo"] for uni in university_list if uni["name"].lower() == short_name),
            "static/logos/default-logo.jpg"
        )

        decision_entry = {
            "short_name": short_name,
            "display_name": display_name,
            "app_type": app_type,
            "decision": display_decision,
            "badge_class": badge_class,
            "release_date": formatted_release_date,
            "logo_url": logo_url
        }

        opened_decisions.append(decision_entry)

    # Debugging: Print all opened_decisions
    print("Opened Decisions:", opened_decisions)

    # Pass data to the template
    return render_template(
        'results.html',
        simulation_started=session.get('simulation_started', False),
        decisions_queue=decisions_queue_sorted,  # Pass sorted decisions
        final_results=final_results,
        read_emails=read_emails,
        name=name,
        app_type=app_type,  # Now correctly set to uppercase or 'Unknown'
        opened_decisions=opened_decisions,  # List of opened decisions
        total_decisions=len(opened_decisions),
        first_unopened=first_unopened,  # Pass first_unopened
        selected_college=selected_college_unique_id  # Pass selected_college for active link highlighting
    )

def format_date(date_str):
    """
    Formats a date string from YYYY-MM-DD to 'Month DD, YYYY'.
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')  # e.g., December 19, 2024
    except ValueError:
        return "Unknown Date"

def schedule_deferred_decision(college_short_name, decisions_queue_sorted):
    """
    Adds a deferred decision as a new status update with the RD release date.
    """
    # Find the college entry
    college_entry = next((c for c in college_list if c[0].lower() == college_short_name.lower()), None)
    if not college_entry:
        print(f"College '{college_short_name}' not found in college_list.")
        return

    # Get the RD release date
    rd_release_date = college_entry[7] if len(college_entry) > 7 else "2099-01-01"
    formatted_rd_release_date = format_date(rd_release_date)

    # Create unique_id for RD
    unique_id = f"{college_short_name}_rd".lower()

    # Check if RD release date is already in the decisions_queue_sorted
    rd_exists = any(
        d.get('unique_id') == unique_id and d.get('release_date') == rd_release_date
        for d in decisions_queue_sorted
    )
    if not rd_exists:
        # Append the deferred RD status update
        new_status_update = {
            "short_name": college_short_name,
            "unique_id": unique_id,
            "display_name": next(
                (uni["display_name"] for uni in university_list if uni["name"].lower() == college_short_name),
                college_short_name.capitalize()
            ),
            "app_type": "RD",  # Regular Decision
            "release_date": rd_release_date,
            "formatted_release_date": formatted_rd_release_date,
            "logo_url": next(
                (uni["logo"] for uni in university_list if uni["name"].lower() == college_short_name),
                "static/logos/default-logo.jpg"
            )
        }
        decisions_queue_sorted.append(new_status_update)
        # Re-sort the decisions_queue_sorted
        try:
            decisions_queue_sorted.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
        except ValueError as e:
            print(f"Error sorting decisions after adding deferred decision: {e}")
            # If sorting fails, do not sort

        print(f"Deferred RD status update added for {college_short_name} with release date {rd_release_date}")

        # Update the session['final_results'] with the RD decision
        if 'final_results' not in session:
            session['final_results'] = {}
        session['final_results'][unique_id] = {
            'decision_code': 'D',
            'app_type': 'RD',
            'release_date': rd_release_date
        }

        # Update the session's 'decisions_queue_sorted'
        session['decisions_queue_sorted'] = decisions_queue_sorted
        session.modified = True  # Ensure the session is marked as modified

# Advanced Simulation Login Route
@app.route("/advancedsim/<college>/login", methods=["GET", "POST"])
def adv_login(college):
    user_data = session.get('advancedsim_data', {"name": "User"})

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate inputs
        if not email or not password:
            flash("Please fill out all fields.", "danger")
            return render_template(
                f"adv/{college}/login.html",
                error="Please fill out all fields.",
                college=college,
                date=user_data.get("date", "N/A"),
                release_date=session.get('release_date', 'Unknown Date')  # Pass release_date if available
            )

        # TODO: Replace the following with actual authentication logic
        success = True  # Placeholder for authentication result

        if success:
            return redirect(url_for('adv_ustatus', college=college))
        else:
            return render_template(
                f"adv/{college}/login.html",
                error="Invalid credentials.",
                college=college,
                date=user_data.get("date", "N/A"),
                release_date=session.get('release_date', 'Unknown Date')  # Pass release_date if available
            )

    # GET request; render the login template
    # Retrieve release_date from final_results
    applied_colleges = session.get('applied_colleges', [])
    unique_id = None
    for college_entry in applied_colleges:
        if college_entry['short_name'] == college.lower():
            unique_id = f"{college_entry['short_name']}_{college_entry['app_type']}".lower()
            break

    decision_info = session.get('final_results', {}).get(unique_id, {})
    release_date_str = decision_info.get('release_date', 'Unknown Date')
    formatted_release_date = format_date(release_date_str)

    print(f"adv_login Route - Release Date for {college}: {release_date_str}")  # Debugging

    return render_template(
        f"adv/{college}/login.html",
        name=user_data.get("name"),
        college=college,
        date=user_data.get("date", "N/A"),
        release_date=formatted_release_date  # Pass release_date to template
    )

# Advanced Simulation Ustatus Route
@app.route("/advancedsim/<college>/ustatus", methods=["GET", "POST"])
@login_required
def adv_ustatus(college):
    # Retrieve user data from 'advancedsim_data'
    user_data = session.get('advancedsim_data', {"name": "User", "date": "N/A"})
    final_results = session.get('final_results', {})

    # Retrieve decision information for the college
    applied_colleges = session.get('applied_colleges', [])
    unique_id = None
    for college_entry in applied_colleges:
        if college_entry['short_name'] == college.lower():
            unique_id = f"{college_entry['short_name']}_{college_entry['app_type']}".lower()
            break

    decision_info = final_results.get(unique_id, {})
    decision_code = decision_info.get('decision_code', 'R')  # Default to 'R' (Rejected) if not found
    release_date_str = decision_info.get('release_date', 'Unknown Date')  # Get release date

    print(f"adv_ustatus Route - Decision Code: {decision_code}, Release Date: {release_date_str}")  # Debugging

    if request.method == "POST":
        # Mark email as read now that user revealed decision
        if 'read_emails' not in session:
            session['read_emails'] = {}
        session['read_emails'][college.lower()] = True
        session.modified = True

        # Redirect to final decision page based on decision_code
        if decision_code == "A":
            return redirect(url_for("adv_acceptance", college=college))
        elif decision_code == "E":
            return redirect(url_for("adv_edacceptance", college=college))
        elif decision_code.startswith("D/"):
            return redirect(url_for("adv_deferred", college=college))
        elif decision_code == "W":
            return redirect(url_for("adv_waitlist", college=college))
        else:
            return redirect(url_for("adv_rejection", college=college))

    # Safely retrieve 'name' from user_data
    name = user_data.get("name", "User")

    # Format the release date
    try:
        date_obj = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')  # e.g., December 19, 2024
    except ValueError:
        formatted_date = "Unknown Date"

    return render_template(
        f"adv/{college}/ustatus.html",
        name=name,
        date=formatted_date,  # Pass the formatted date
        college=college,
        decision_code=decision_code  # Pass decision_code for template use
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

# Acceptance Route
@app.route("/advancedsim/<college>/acceptance")
@login_required
def adv_acceptance(college):
    user_id = session.get('user_id')
    final_results = session.get('final_results', {})
    
    unique_id = f"{college.lower()}_a".lower()  # Adjust based on your unique_id formation

    decision_info = final_results.get(unique_id, {})
    decision_code = decision_info.get('decision_code', 'A')  # 'A' for acceptance
    release_date_str = decision_info.get('release_date', 'Unknown Date')

    if user_id:
        User.log_simulation(user_id, college, 'acceptance')

    # Format the release date
    try:
        date_obj = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    print(f"adv_acceptance Route - Release Date for {college}: {release_date_str}")  # Debugging

    return render_template(
        f"adv/{college}/acceptance.html",
        name=session.get("advancedsim_data", {}).get("name", "User"),
        date=formatted_date,
        college=college
    )

# Early Decision Acceptance Route
@app.route("/advancedsim/<college>/edacceptance", methods=["GET", "POST"])
@login_required
def adv_edacceptance(college):
    user_id = session.get('user_id')
    final_results = session.get('final_results', {})
    
    unique_id = f"{college.lower()}_e".lower()  # Adjust based on your unique_id formation

    decision_info = final_results.get(unique_id, {})
    decision_code = decision_info.get('decision_code', 'E')  # 'E' for ED acceptance
    release_date_str = decision_info.get('release_date', 'Unknown Date')

    if user_id:
        User.log_simulation(user_id, college, 'ed_acceptance')

    # Format the release date
    try:
        date_obj = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    print(f"adv_edacceptance Route - Release Date for {college}: {release_date_str}")  # Debugging

    return render_template(
        f"adv/{college}/edacceptance.html",
        name=session.get("advancedsim_data", {}).get("name", "User"),
        date=formatted_date,
        college=college
    )

# Rejection Route
@app.route("/advancedsim/<college>/rejection")
@login_required
def adv_rejection(college):
    user_id = session.get('user_id')
    final_results = session.get('final_results', {})
    
    unique_id = f"{college.lower()}_r".lower()  # Adjust based on your unique_id formation

    decision_info = final_results.get(unique_id, {})
    decision_code = decision_info.get('decision_code', 'R')  # 'R' for rejection
    release_date_str = decision_info.get('release_date', 'Unknown Date')

    if user_id:
        User.log_simulation(user_id, college, 'rejection')

    # Format the release date
    try:
        date_obj = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    print(f"adv_rejection Route - Release Date for {college}: {release_date_str}")  # Debugging

    return render_template(
        f"adv/{college}/rejection.html",
        name=session.get("advancedsim_data", {}).get("name", "User"),
        date=formatted_date,
        college=college
    )

# Deferred Route
@app.route("/advancedsim/<college>/deferred")
@login_required
def adv_deferred(college):
    user_id = session.get('user_id')
    final_results = session.get('final_results', {})
    
    unique_id = f"{college.lower()}_d".lower()  # Adjust based on your unique_id formation

    decision_info = final_results.get(unique_id, {})
    decision_code = decision_info.get('decision_code', 'D')  # 'D' for deferred
    release_date_str = decision_info.get('release_date', 'Unknown Date')

    if user_id:
        User.log_simulation(user_id, college, 'deferred')

    # Format the release date
    try:
        date_obj = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    print(f"adv_deferred Route - Release Date for {college}: {release_date_str}")  # Debugging

    return render_template(
        f"adv/{college}/deferred.html",
        name=session.get("advancedsim_data", {}).get("name", "User"),
        date=formatted_date,
        college=college
    )

# Waitlist Route
@app.route("/advancedsim/<college>/waitlist")
@login_required
def adv_waitlist(college):
    user_id = session.get('user_id')
    final_results = session.get('final_results', {})
    
    unique_id = f"{college.lower()}_w".lower()  # Adjust based on your unique_id formation

    decision_info = final_results.get(unique_id, {})
    decision_code = decision_info.get('decision_code', 'W')  # 'W' for waitlist
    release_date_str = decision_info.get('release_date', 'Unknown Date')

    if user_id:
        User.log_simulation(user_id, college, 'waitlist')

    # Format the release date
    try:
        date_obj = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    print(f"adv_waitlist Route - Release Date for {college}: {release_date_str}")  # Debugging

    return render_template(
        f"adv/{college}/waitlist.html",
        name=session.get("advancedsim_data", {}).get("name", "User"),
        date=formatted_date,
        college=college
    )

@app.route('/quicksim/<college>/login_files/<path:filename>')
def login_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'login_files'), filename)

@app.route('/quicksim/<college>/ustatus_files/<path:filename>')
def ustatus_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'ustatus_files'), filename)

@app.route('/quicksim/<college>/acceptance_files/<path:filename>')
def acceptance_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'acceptance_files'), filename)

@app.route('/quicksim/<college>/ball_images/<path:filename>')
def ball_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'ball_images'), filename)

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

if __name__ == "__main__":
    app.run(debug=True)
    