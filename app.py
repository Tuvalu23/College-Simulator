import random
from datetime import datetime
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
    ["columbia", "0.02", "1.9", "N", "P"],
    ["stanford", "0.03", "N", "1.3", "REA"],
    ["upenn", "0.03", "2.3", "N", "P"],
    ["caltech", "0.03", "N", "1.1", "REA"],
    ["princeton", "0.06", "N", "1.3", "REA"],
    ["mit", "0.06", "N", "1.2", "P"],
    ["yale", "0.07", "N", "1.3", "REA"],
    ["harvard", "0.08", "N", "1.3", "REA"],
    ["uchicago", "0.08", "2.5", "1.3", "P"],
    ["jhu", "0.05", "1.7", "N", "P"],
    ["dartmouth", "0.09", "2.3", "N", "P"],
    ["brown", "0.09", "2.0", "N", "P"],
    ["duke", "0.10", "2.0", "N", "P"],
    ["northwestern", "0.12", "2.2", "N", "P"],
    ["cornell", "0.18", "2.2", "N", "P"],
    ["umich", "0.18", "N", "1.3", "PUB"],
    ["berkeley", "0.15", "N", "N", "PUB"],
    ["usc", "0.17", "N", "1.3", "P"],
    ["University of Virginia (UVA)", "0.15", "N", "1.3", "PUB"],
    ["nyu", "0.22", "1.5", "N", "P"],
    ["gtech", "0.16", "N", "1.4", "PUB"],
    ["bing", "0.70", "N", "1.3", "PUB"]
]

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
@app.route("/universities", methods=["GET", "POST"])
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

@app.route("/<college>/login", methods=["GET", "POST"])
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
@app.route("/<college>/ustatus", methods=["GET", "POST"])
def ustatus(college):
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    if request.method == "POST":
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college))
        return redirect(url_for("rejection", college=college))
    return render_template(f"{college}/ustatus.html", name=user_data["name"], date=user_data["date"], college=college)

@app.route("/<college>/acceptance")
def acceptance(college):
    user_id = session.get('user_id')
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    if user_id:
        User.log_simulation(user_id, college, 'acceptance')
    return render_template(f"{college}/acceptance.html", name=user_data["name"], date=user_data["date"], college=college)

@app.route("/<college>/rejection")
def rejection(college):
    user_id = session.get('user_id')
    user_data = session.get('quicksim_data', {"name": "User", "date": "N/A"})
    if user_id:
        User.log_simulation(user_id, college, 'rejection')
    return render_template(f"{college}/rejection.html", name=user_data["name"], date=user_data["date"], college=college)

# advanced sm stuff
submissions = []

@app.route("/advancedsim", methods=["GET", "POST"])
@login_required
def advancedsim():
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
        race = request.form.get("race", "").strip()
        gender = request.form.get("gender", "").strip()
        first_gen = request.form.get("first_gen", "off") == "on"

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

        if not race:
            error = True
            error_messages.append("Race/Ethnicity selection is required.")

        if not gender:
            error = True
            error_messages.append("Gender selection is required.")

        if error:
            for message in error_messages:
                flash(message)
            # Optionally, you can repopulate the form with previously entered data here
            return render_template("advancedsim.html")
        
        # If all validations pass, store the submission
        submission_data = {
            "name": name,
            "gpa": gpa_val,
            "test_option": test_option,
            "sat_score": sat_val if test_option == 'sat' else None,
            "act_score": act_val if test_option == 'act' else None,
            "extracurriculars": extracurriculars_val,
            "essays": essays_val,
            "ap_courses": ap_val,
            "race": race,
            "gender": gender,
            "first_gen": first_gen,
        }
        submissions.append(submission_data)

        flash("Application submitted successfully!", "success")
        # Redirect to a success page or the same form
        return redirect(url_for("earlydecision"))

    return render_template("advancedsim.html")

@app.route('/earlydecision', methods=['GET', 'POST'])
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
                session['selected_schools'].append(ed_school)  # Add ED school to the list
                session.modified = True
                return redirect(url_for('earlyaction'))  # Skip REA, go to EA
            else:
                flash("Please select an Early Decision school.", "danger")
        else:  # User selects No
            session['ed_school'] = None
            return redirect(url_for('rea'))  # Proceed to REA

    # Filter ED schools: ED available if column[2] != "N"
    ed_schools = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0])
        }
        for u in college_list if u[2] != "N"
    ]

    return render_template('earlydecision.html', ed_schools=ed_schools)

@app.route('/rea', methods=['GET', 'POST'])
@login_required
def rea():
    if request.method == 'POST':
        rea_choice = request.form.get('rea_choice')
        session['rea_choice'] = rea_choice
        if rea_choice == 'yes':
            rea_school = request.form.get('rea_school')  # User selects one REA school
            if rea_school:
                session['rea_school'] = rea_school
                session['selected_schools'].append(rea_school)  # Add REA school to the list
                session.modified = True  # Mark session as modified
                return redirect(url_for('earlyaction'))
            else:
                flash("Please select a Restricted Early Action school.", "danger")
        else:
            session['rea_school'] = None
            return redirect(url_for('earlyaction'))

    # Filter REA schools: column[4] == "REA"
    rea_schools = [u for u in college_list if u[4] == "REA"]

    return render_template('rea.html', rea_schools=rea_schools)

@app.route('/earlyaction', methods=['GET', 'POST'])
@login_required
def earlyaction():
    if request.method == 'POST':
        ea_schools_selected = request.form.getlist('ea_schools')  # Multiple EA schools
        session['ea_schools'] = ea_schools_selected
        session['selected_schools'].extend(ea_schools_selected)  # Add EA schools to the list
        session.modified = True  # Mark session as modified
        return redirect(url_for('regulardecision'))

    chosen_ed = session.get('ed_school')
    chosen_rea = session.get('rea_school')

    # Exclude ED and REA chosen from the list
    chosen = [c for c in [chosen_ed, chosen_rea] if c]

    # If REA chosen, only public EA schools
    if chosen_rea:
        ea_schools = [u for u in college_list if u[0] not in chosen and u[4] == "PUB"]
    else:
        # Show both private (P) and public (PUB) schools not chosen yet
        ea_schools = [u for u in college_list if u[0] not in chosen and (u[4] == "P" or u[4] == "PUB")]

    # Exclude ED schools from EA if ED was chosen
    if chosen_ed:
        ea_schools = [u for u in ea_schools if u[0] != chosen_ed]

    return render_template('earlyaction.html', ea_schools=ea_schools)

@app.route('/regulardecision', methods=['GET', 'POST'])
@login_required
def regulardecision():
    if request.method == 'POST':
        rd_schools_selected = request.form.getlist('rd_schools')  # Multiple RD schools
        session['rd_schools'] = rd_schools_selected
        session['selected_schools'].extend(rd_schools_selected)  # Add RD schools to the list
        session.modified = True  # Mark session as modified

        # Display confirmation or redirect to a summary page
        return redirect(url_for('summary'))

    chosen_all = session.get('selected_schools', [])

    # RD shows all not chosen yet in ED/REA/EA
    rd_schools = [u for u in college_list if u[0] not in chosen_all]

    return render_template('regulardecision.html', rd_schools=rd_schools)

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

@app.route('/advancedsim_files/<path:filename>')
def advanced_files_static(filename):
    file_directory = os.path.join(app.root_path, 'templates', 'advancedsim_files')
    return send_from_directory(file_directory, filename)


if __name__ == "__main__":
    app.run(debug=True)
    