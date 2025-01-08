import random
from datetime import datetime, timedelta
import os
import logging

from flask import Flask, render_template, redirect, request, url_for, send_from_directory, session, flash, jsonify
from functools import wraps
from models import init_db, User

app = Flask(__name__, template_folder="templates")
app.secret_key = 'Tuvalu23'

# init db
init_db()

# max colleges u can apply to
MAX_COLLEGES = 25

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        {"label": "Faith-Based", "color": "Faith-Based"},
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
    "name": "illini",
    "display_name": "University of Illinois Urbana-Champaign",
    "logo": "static/logos/illini-logo.png",
    "description": "The University of Illinois Urbana-Champaign is a premier public research institution known for its pioneering work in engineering, computer science, and business. Located in the heart of Illinois, it offers a vibrant campus and college experience.",
    "badges": [
        {"label": "Public", "color": "Public"},
        {"label": "Big Ten", "color": "Big Ten"},
        {"label": "Engineering", "color": "Engineering"},
        {"label": "Innovation", "color": "Innovation"},
        {"label": "Global", "color": "Global"},
        {"label": "Inclusive", "color": "Inclusive"}
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
            {"label": "Big Ten", "color": "Big Ten"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Research", "color": "Research"},
            {"label": "Performing Arts", "color": "Performing Arts"},
            {"label": "Media", "color": "Media"}
        ]
    },
    {
    "name": "notredame",
    "display_name": "University of Notre Dame",
    "logo": "static/logos/notredame-logo.png",
    "description": "The University of Notre Dame, located in South Bend, IN, is a prestigious Catholic institution renowned for its commitment to academic excellence, community service, and faith-based education.",
    "badges": [
        {"label": "T-20", "color": "T-20"},
        {"label": "Private", "color": "Private"},
        {"label": "Suburban", "color": "Suburban"},
        {"label": "Faith-Based", "color": "Faith-Based"},
        {"label": "Research", "color": "Research"},
        {"label": "Tradition", "color": "Tradition"},
        {"label": "Athletics", "color": "Athletics"},
        {"label": "Community", "color": "Community"}
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
    "name": "purdue",
    "display_name": "Purdue University",
    "logo": "static/logos/purdue-logo.png",
    "description": "Purdue University, located in West Lafayette, IN, is a top public research institution known for its strong engineering, agriculture, and technology programs. It offers a vibrant campus community and a commitment to academic excellence and innovation.",
    "badges": [
        {"label": "Public", "color": "Public"},
        {"label": "Big Ten", "color": "Big Ten"},
        {"label": "Engineering", "color": "Engineering"},
        {"label": "Agriculture", "color": "Agriculture"},
        {"label": "Technology", "color": "Technology"},
        {"label": "Research", "color": "Research"},
        {"label": "Value", "color": "Value"}
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
    "name": "ucla",
    "display_name": "University of California, Los Angeles",
    "logo": "static/logos/ucla-logo.png",
    "description": "The University of California, Los Angeles, is a top-ranked public research university known for its excellence in academics, athletics, and innovation.",
    "badges": [
        {"label": "T-20", "color": "T-20"},
        {"label": "Public", "color": "Public"},
        {"label": "Big Ten", "color": "Big Ten"},
        {"label": "Urban", "color": "Urban"},
        {"label": "Research", "color": "Research"},
        {"label": "Diverse", "color": "Diverse"},
        {"label": "Athletics", "color": "Athletics"}
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
        "name": "umich",
        "display_name": "University of Michigan",
        "logo": "static/logos/umich-logo.png",
        "description": "The University of Michigan in Ann Arbor, MI, is a leading public research university known for its vibrant academic environment and outstanding athletic programs. It offers an array of programs across humanities, engineering, and business.",
        "badges": [
            {"label": "T-20", "color": "T-20"},
            {"label": "Public", "color": "Public"},
            {"label": "Big Ten", "color": "Big Ten"},
            {"label": "Suburban", "color": "Suburban"},
            {"label": "Research", "color": "Research"},
            {"label": "Athletics", "color": "Athletics"},
            {"label": "Business", "color": "Business"},
            {"label": "Diverse", "color": "Diverse"}
        ]
    },
    {
    "name": "unc",
    "display_name": "University of North Carolina at Chapel Hill",
    "logo": "static/logos/unc-logo.png",
    "description": "The University of North Carolina at Chapel Hill, often referred to as UNC or Carolina, is renowned for its innovative research, strong public health programs, and spirited Tar Heel athletics.",
    "badges": [
        {"label": "T-30", "color": "T-30"},
        {"label": "Public", "color": "Public"},
        {"label": "Research", "color": "Research"},
        {"label": "Athletics", "color": "Athletics"},
        {"label": "Health Sciences", "color": "Health Sciences"},
        {"label": "Diverse", "color": "Diverse"}
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
    "name": "utexas",
    "display_name": "University of Texas at Austin",
    "logo": "static/logos/utexas-logo.png",
    "description": "The University of Texas at Austin, located in Austin, TX, is a renowned public research university known for its spirited campus culture, top-tier academic programs, and dynamic connection to the vibrant city of Austin.",
    "badges": [
        {"label": "Public", "color": "Public"},
        {"label": "Urban", "color": "Urban"},
        {"label": "STEM", "color": "STEM"},
        {"label": "Business", "color": "Business"},
        {"label": "Research", "color": "Research"},
        {"label": "Arts", "color": "Arts"},
        {"label": "Athletics", "color": "Athletics"},
        {"label": "Hook 'Em", "color": "Hook 'Em"}
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
            {"label": "Big Ten", "color": "Big Ten"},
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
    "name": "washu",
    "display_name": "Washington University in St. Louis",
    "logo": "static/logos/washu-logo.jpg",
    "description": "Washington University in St. Louis, located in St. Louis, MO, is a prestigious private research institution renowned for its interdisciplinary academic programs, close-knit campus community, and emphasis on innovation and collaboration.",
    "badges": [
        {"label": "T-30", "color": "T-30"},
        {"label": "Private", "color": "Private"},
        {"label": "Urban", "color": "Urban"},
        {"label": "Collaborative", "color": "Collaborative"},
        {"label": "Health Sciences", "color": "Health Sciences"},
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
    ["caltech", "0.03", "N", "1.1", "REA", "2024-12-12", "N", "2025-03-09"],
    ["jhu", "0.05", "1.7", "N", "P", "2024-12-13", "N", "2025-03-20"],
    ["dartmouth", "0.05", "2.3", "N", "P", "2024-12-13", "N", "2025-03-28"],
    ["princeton", "0.06", "N", "1.3", "REA", "2024-12-12", "N", "2025-03-28"],
    ["mit", "0.06", "N", "1.2", "P", "N", "2024-12-17", "2025-03-14"],
    ["yale", "0.07", "N", "1.3", "REA", "2024-12-17", "N", "2025-03-28"],
    ["harvard", "0.07", "N", "1.3", "REA", "2024-12-12", "N", "2025-03-28"],
    ["brown", "0.07", "2.0", "N", "P", "2024-12-13", "N", "2025-03-28"],
    ["notredame", "0.08", "N", "1.2", "REA", "2024-12-17", "N", "2025-03-15"],
    ["uchicago", "0.09", "2.5", "1.1", "P", "2024-12-20", "2024-12-20", "2025-03-25"],
    ["northwestern", "0.09", "2.2", "N", "P", "2024-12-17", "N", "2025-03-27"],
    ["duke", "0.09", "2.0", "N", "P", "2024-12-16", "N", "2025-03-28"],
    ["cmu", "0.10", "1.2", "N", "P", "2024-12-13", "N", "2025-03-21"],
    ["rice", "0.12", "2", "N", "P", "2024-12-14", "N", "2025-03-21"],
    ["washu", "0.12", "1.6", "N", "P", "2024-12-12", "N", "2025-03-13"],
    ["tufts", "0.14", "2.0", "N", "P", "2024-12-13", "N", "2025-03-22"],
    ["northeastern", "0.15", "2.7", "1.3", "P", "2024-12-11", "2025-01-31", "2025-03-17"],
    ["cornell", "0.15", "2.2", "N", "P", "2024-12-12", "N", "2025-03-28"],
    ["uva", "0.15", "2.3", "1.3", "PUB", "2024-12-13", "2025-2-15", "2025-03-21"],
    ["gtech", "0.15", "N", "1.4", "PUB", "N", "2025-01-27", "2025-03-22"],
    ["berkeley", "0.15", "N", "N", "PUB", "N", "N", "2025-03-27"],
    ["ucla", "0.15", "N", "N", "P", "N", "N", "2025-03-21"],
    ["emory", "0.16", "1.7", "N", "P", "2024-12-11", "N", "2025-03-27"],
    ["usc", "0.17", "N", "1.3", "P", "N", "2025-01-17", "2025-03-16"],
    ["umich", "0.2", "N", "1.3", "PUB", "N", "2025-01-27", "2025-03-30"],
    ["utexas", "0.2", "N", "1.2", "PUB", "N", "2025-01-15", "2025-02-15"],
    ["nyu", "0.22", "1.5", "N", "P", "2024-12-12", "N", "2025-03-28"],
    ["georgetown", "0.23", "N", "1.3", "REA", "2024-12-13", "N", "2025-03-27"],
    ["illini", "0.24", "N", "1.2", "PUB", "N", "2025-01-31", "2025-02-28"],
    ["unc", "0.24", "N", "1.3", "PUB", "N", "2025-01-26", "2025-03-06"],
    ["purdue", "0.5", "N", "1.3", "PUB", "N", "2025-1-15", "2025-03-01"],
    ["bing", "0.55", "N", "1.3", "PUB", "N", "2024-11-20", "2025-02-15"],
    ["buffalo", "0.75", "N", "1.2", "PUB", "N", "2024-11-15", "2025-02-10"]
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
                      + len([sim for sim in uni_simulations if sim['result'] == 'edacceptance']) + len([sim for sim in uni_simulations if sim['result'] == 'wacceptance'])
        rejections = len([sim for sim in uni_simulations if sim['result'] == 'rejection']) + len([sim for sim in uni_simulations if sim['result'] == 'wrejection'])
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
        # Simulate decision upon form submission
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college))
        else:
            return redirect(url_for("rejection", college=college))
    
    if college.lower() == "northeastern" or college.lower() == "utexas" or college.lower() == "ucla":
        # Simulate decision directly
        decision = random.choice(["acceptance", "rejection"])
        if decision == "acceptance":
            return redirect(url_for("acceptance", college=college))
        else:
            return redirect(url_for("rejection", college=college))
    else:
        # For other colleges, render the ustatus template
        return render_template(f"{college}/ustatus.html", name=user_data["name"], college=college, date=user_data["date"])

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

# Define US_STATES as shown earlier
US_STATES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

# Advanced Simulation Route
@app.route("/advancedsim", methods=["GET", "POST"])
@login_required
def advancedsim():
    clear_session()
    if request.method == "POST":
        # Extract form data
        name = request.form.get("name", "").strip()
        state = request.form.get("state", "").strip()
        legacy = request.form.get("legacy", "").strip() 
        gpa = request.form.get("gpa", "").strip()
        test_option = request.form.get("test_option", "")
        sat_score = request.form.get("sat_score", "").strip()
        act_score = request.form.get("act_score", "").strip()
        extracurriculars = request.form.get("extracurriculars", "").strip()
        essays = request.form.get("essays", "").strip()
        lors = request.form.get("lors", "").strip()
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
            extracurriculars_val = float(extracurriculars)
            if not (0 <= extracurriculars_val <= 10):
                raise ValueError
        except ValueError:
            error = True
            error_messages.append("Extracurricular activities rating must be between 0 and 10.")

        try:
            essays_val = float(essays)
            if not (0 <= essays_val <= 10):
                raise ValueError
        except ValueError:
            error = True
            error_messages.append("Essays rating must be between 0 and 10.")
            
        try:
            lors_val = float(lors)
            if not (0 <= lors_val <= 10):
                raise ValueError
        except ValueError:
            error = True
            error_messages.append("LORS rating must be between 0 and 10.")

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
                score -= 3
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
        essay_category, essay_class = rate(essays_val)          # Correct Order
        extra_category, extra_class = rate(extracurriculars_val)
        lors_category, lors_class = rate(lors_val)

        # Add demographic score and category to submission_data
        submission_data = {
    "name": name,
    "state": state, 
    "legacy": legacy,
    "gpa": gpa_val,
    "test_option": test_option,
    "sat_score": sat_val if test_option == 'sat' else None,
    "act_score": act_val if test_option == 'act' else None,
    "extracurriculars": extracurriculars_val,
    "essays": essays_val,
    "lors": lors_val,
    "ap_courses": ap_val,
    "race": race,       # Stored as integer code
    "gender": gender,   # Stored as integer code
    "first_gen": first_gen,
    "dem_score": dem_score,          # Store Demographic Score
    "dem_category": dem_category,    # Store Demographic Category
    "dem_class": dem_class,          # Store CSS Class for Category
    "essay_category": essay_category, # Corrected Order
    "essay_class": essay_class,        # Corrected Order
    "lors_category": lors_category,
    "lors_class": lors_class,
    "extra_category": extra_category,   # Corrected Key
    "extra_class": extra_class,         # Corrected Key
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
    """
    Adds a school to the session's selected_schools if not already present and within the limit.
    Returns True if added, False otherwise.
    """
    if 'selected_schools' not in session:
        session['selected_schools'] = []

    # Normalize school name to lowercase for consistency
    school_lower = school.lower()

    if school_lower not in [s.lower() for s in session['selected_schools']]:
        if len(session['selected_schools']) >= MAX_COLLEGES:
            print(f"Cannot add {school}: maximum of {MAX_COLLEGES} colleges reached.")
            return False
        session['selected_schools'].append(school)
        session.modified = True
        print(f"Added school: {school}")
    else:
        print(f"School already selected: {school}")
    return True

def remove_school(school):
    """
    Removes a school from the session's selected_schools if present.
    """
    if 'selected_schools' in session:
        # Normalize school name to lowercase for consistency
        session['selected_schools'] = [s for s in session['selected_schools'] if s.lower() != school.lower()]
        session.modified = True
        print(f"Removed school: {school}")
    else:
        print(f"No schools selected to remove.")
    
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
                success = add_school(ed_school)  # Attempt to add ED school to the list

                if not success:
                    flash(f"You can only apply to a maximum of {MAX_COLLEGES} colleges. Please remove a college before adding another.", "warning")
                    return redirect(url_for('earlydecision'))

                session['ed_school'] = ed_school

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
                return redirect(url_for('earlydecision'))  # Return to ED selection

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

    # Determine if the user has reached the maximum limit
    current_count = len(session.get('selected_schools', []))
    limit_reached = current_count >= MAX_COLLEGES

    # Filter ED schools: ED available if column[2] != "N" and not already selected
    ed_schools = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0]),
            "disabled": limit_reached and u[0] not in session.get('selected_schools', [])
        }
        for u in college_list if u[2] != "N" and u[0] not in session.get('selected_schools', [])
    ]

    return render_template('earlydecision.html', ed_schools=ed_schools, limit_reached=limit_reached)

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
                success = add_school(rea_school)  # Attempt to add REA school to the list

                if not success:
                    flash(f"You can only apply to a maximum of {MAX_COLLEGES} colleges. Please remove a college before adding another.", "warning")
                    return redirect(url_for('rea'))

                session['rea_school'] = rea_school

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

    # Determine if the user has reached the maximum limit
    current_count = len(session.get('selected_schools', []))
    limit_reached = current_count >= MAX_COLLEGES

    # Filter REA schools: column[4] == "REA" and u[3] != "N" and not already selected
    rea_schools = [
        {
            "name": u[0],
            "display_name": next((uni["display_name"] for uni in university_list if uni["name"] == u[0]), u[0]),
            "disabled": limit_reached and u[0] not in session.get('selected_schools', [])
        }
        for u in college_list if u[4] == "REA" and u[3] != "N" and u[0] not in session.get('selected_schools', [])
    ]

    return render_template('rea.html', rea_schools=rea_schools, limit_reached=limit_reached)

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
                remaining_slots = MAX_COLLEGES - get_already_applied_count()
                ea_schools_prepared = prepare_ea_schools(remaining_slots)
                ea_schools_lower = [s.lower() for s in session.get('ea_schools', [])]
                return render_template(
                    'earlyaction.html',
                    ea_schools=ea_schools_prepared,
                    limit_reached=(remaining_slots <= 0),
                    already_selected_count=get_already_applied_count(),
                    ea_schools_lower=ea_schools_lower,
                    max_colleges=MAX_COLLEGES
                )

            # Calculate remaining slots
            already_applied = get_already_applied_count()
            remaining_slots = MAX_COLLEGES - already_applied

            if len(ea_schools_selected) > remaining_slots:
                flash(f"You can only apply to {remaining_slots} more college(s). Please remove some selections or choose fewer schools.", "warning")
                ea_schools_prepared = prepare_ea_schools(remaining_slots)
                ea_schools_lower = [s.lower() for s in session.get('ea_schools', [])]
                return render_template(
                    'earlyaction.html',
                    ea_schools=ea_schools_prepared,
                    limit_reached=(remaining_slots <= 0),
                    already_selected_count=already_applied,
                    ea_schools_lower=ea_schools_lower,
                    max_colleges=MAX_COLLEGES
                )

            # Prevent duplicates and enforce limit
            for school in ea_schools_selected:
                success = add_school(school)
                if not success:
                    flash(f"Cannot add {school}: maximum of {MAX_COLLEGES} colleges reached.", "warning")
                    break  # Stop adding more schools

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
            return redirect(url_for('earlyaction'))  # Adjust as per your flow

    # GET request handling

    already_applied = get_already_applied_count()
    remaining_slots = MAX_COLLEGES - already_applied

    # Prepare EA schools list based on remaining_slots
    ea_schools_prepared = prepare_ea_schools(remaining_slots)

    # Determine if the user has reached the maximum limit
    limit_reached = remaining_slots <= 0

    # Precompute 'ea_schools_lower' for template (for case-insensitive comparison)
    ea_schools_lower = [s.lower() for s in session.get('ea_schools', [])]

    return render_template(
        'earlyaction.html',
        ea_schools=ea_schools_prepared,
        limit_reached=limit_reached,
        already_selected_count=already_applied,
        ea_schools_lower=ea_schools_lower,
        max_colleges=MAX_COLLEGES
    )

# Helper Function to Prepare EA Schools
def prepare_ea_schools(remaining_slots):
    """
    Prepares the list of Early Action schools with their disabled status based on remaining_slots.
    """
    chosen_ed = session.get('ed_school')
    chosen_rea = session.get('rea_school')
    chosen_ea = session.get('ea_schools', [])

    # Exclude ED, REA, and already selected EA schools from the list
    excluded_schools = set(filter(None, [chosen_ed, chosen_rea])) | set(chosen_ea)

    # If REA is chosen, only public EA schools and u[3] != "N"
    if chosen_rea:
        filtered_colleges = [
            u for u in college_list 
            if u[0].lower() not in [s.lower() for s in excluded_schools] and u[4] == "PUB" and u[3] != "N"
        ]
    else:
        # Show both private (P) and public (PUB) schools not chosen yet and u[3] != "N"
        filtered_colleges = [
            u for u in college_list 
            if u[0].lower() not in [s.lower() for s in excluded_schools] and u[4] in ["P", "PUB"] and u[3] != "N"
        ]

    # Disable if no remaining slots
    disabled = remaining_slots <= 0

    # Prepare EA schools as list of dictionaries
    ea_schools = [
        {
            "name": u[0],
            "display_name": next(
                (uni["display_name"] for uni in university_list if uni["name"].lower() == u[0].lower()),
                u[0]
            ),
            "disabled": disabled
        }
        for u in filtered_colleges
    ]

    return ea_schools

def get_already_applied_count():
    """
    Calculates the number of schools already applied to across ED, REA, and EA.
    """
    count = 0
    if session.get('ed_school'):
        count += 1
    if session.get('rea_school'):
        count += 1
    count += len(session.get('ea_schools', []))
    return count


# Regular Decision Route
@app.route('/advancedsim/regulardecision', methods=['GET', 'POST'])
@login_required
def regulardecision():
    if 'selected_schools' not in session:
        session['selected_schools'] = []  # Initialize if not present

    already_applied = get_already_applied_count()
    remaining_slots = MAX_COLLEGES - already_applied

    if request.method == 'POST':
        rd_schools_selected = request.form.getlist('rd_schools')  # List of selected RD schools

        # Server-side validation
        if len(rd_schools_selected) > remaining_slots:
            flash(f"You can only apply to {remaining_slots} more college(s). Please remove some selections or choose fewer schools.", "warning")
            rd_schools_prepared = prepare_rd_schools(remaining_slots)
            rd_schools_lower = [s.lower() for s in rd_schools_selected]
            return render_template(
                'regulardecision.html',
                rd_schools=rd_schools_prepared,
                rd_schools_lower=rd_schools_lower,
                limit_reached=(remaining_slots <= 0),
                already_selected_count=already_applied,
                max_colleges=MAX_COLLEGES
            )

        if 'rd_choice' in request.form and request.form.get('rd_choice') == 'yes' and len(rd_schools_selected) == 0:
            flash("Please select at least one Regular Decision school.", "danger")
            rd_schools_prepared = prepare_rd_schools(remaining_slots)
            rd_schools_lower = []
            return render_template(
                'regulardecision.html',
                rd_schools=rd_schools_prepared,
                rd_schools_lower=rd_schools_lower,
                limit_reached=(remaining_slots <= 0),
                already_selected_count=already_applied,
                max_colleges=MAX_COLLEGES
            )

        # Add RD schools to 'selected_schools' and to session['rd_schools']
        for school in rd_schools_selected:
            add_school(school)

        session['rd_schools'] = rd_schools_selected
        session.modified = True

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
            return redirect(url_for('earlyaction'))  # Adjust as per your flow

    # GET request handling

    # already_applied and remaining_slots are already computed above

    # Prepare RD schools list based on remaining_slots
    rd_schools_prepared = prepare_rd_schools(remaining_slots)
    rd_schools_lower = [s.lower() for s in session.get('rd_schools', [])]

    # Determine if the user has reached the maximum limit
    limit_reached = remaining_slots <= 0

    return render_template(
        'regulardecision.html',
        rd_schools=rd_schools_prepared,
        rd_schools_lower=rd_schools_lower,
        limit_reached=limit_reached,
        already_selected_count=already_applied,
        max_colleges=MAX_COLLEGES
    )
    
def prepare_rd_schools(remaining_slots):
    """
    Prepares the list of Regular Decision schools with their disabled status based on remaining_slots.
    """
    rd_schools_available = [
        u for u in college_list 
        if u[0].lower() not in [school.lower() for school in session.get('selected_schools', [])]
    ]
    rd_schools_prepared = []

    for college in rd_schools_available:
        short_name = college[0]
        display_name = next(
            (uni["display_name"] for uni in university_list if uni["name"].lower() == short_name.lower()),
            short_name
        )
        # Disable if no remaining slots
        disabled = remaining_slots <= 0
        rd_schools_prepared.append({
            "name": short_name,
            "display_name": display_name,
            "disabled": disabled
        })

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
        "State": user_data.get("state", "N/A"),
        "Legacy": user_data.get("legacy", "None"),
        "GPA": user_data.get("gpa", "N/A"),
        "Test Option": user_data.get("test_option", "N/A").upper(),
        "SAT Score": user_data.get("sat_score", "N/A") if user_data.get("test_option") == 'sat' else "N/A",
        "ACT Score": user_data.get("act_score", "N/A") if user_data.get("test_option") == 'act' else "N/A",
        "Extracurricular Activities": user_data.get("extracurriculars", "N/A"),
        "Essays Rating": user_data.get("essays", "N/A"),
        "Letters of Recommendation Rating": user_data.get("lors", "N/A"),
        "LORS Category": user_data.get("lors_category", "N/A"),
        "LORS Class": user_data.get("lors_class", "na"),
        "AP Courses Taken": user_data.get("ap_courses", "N/A"),
        "Race/Ethnicity": user_data.get("race", "N/A"),
        "Gender": user_data.get("gender", "N/A"),
        "First Generation": "Yes" if user_data.get("first_gen") else "No",
        "Demographic Score": user_data.get("dem_score", "N/A"),
        "Demographic Category": user_data.get("dem_category", "N/A"),
        "Demographic Class": user_data.get("dem_class", "na"),
        "Essay Category": user_data.get("essay_category", "N/A"),
        "Essay Class": user_data.get("essay_class", "na"),
        "Extra Category": user_data.get("extra_category", "N/A"),
        "Extra Class": user_data.get("extra_class", "na"),
        "Weighted GPA": user_data.get("wgpa", "N/A")
    }
    
    state_abbr = user_data.get("state", "N/A")
    state_full = US_STATES.get(state_abbr, "N/A") if state_abbr != "N/A" else "N/A"
    
    legacy_name = user_data.get("legacy", "none")
    
    r_legacy = next(
    (uni['display_name'] for uni in university_list if uni['name'] == legacy_name),
    "None"  # Default value if no match is found
)


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
        decisions_queue=decisions_queue_sorted, state_full=state_full,
        r_legacy=r_legacy
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
        return "Likely", "likely"
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
    # Define classification based on student_num with 15 tiers and curved intervals
    if student_num >= 103:
        return 1
    elif student_num >= 96:
        return 2
    elif student_num >= 90:
        return 3
    elif student_num >= 85:
        return 4
    elif student_num >= 80:
        return 5
    elif student_num >= 75:
        return 6
    elif student_num >= 70:
        return 7
    elif student_num >= 65:
        return 8
    elif student_num >= 60:
        return 9
    elif student_num >= 52:
        return 10
    elif student_num >= 43:
        return 11
    elif student_num >= 34:
        return 12
    elif student_num >= 25:
        return 13
    elif student_num >= 15:
        return 14
    else:
        return 15  # Anything below 15 falls into the lowest tier
    
def chanceCollege(collegeList, i, demScore, testOptional, sat, act, extracurriculars, ap_courses, essayStrength, gpa, interviewStrength, app_type, state, legacy, lors):
    baseChance = float(collegeList[i][1]) * 100  # Acceptance rate as percentage (0-100)
    interviewScore = interviewStrength

    student_num = 0.0
    if testOptional:
        # Full: GPA = 40 pts, EC = 20 pts, Essay = 20 pts, AP = 10 pts, Interview = 10 pts, LORS: 10pts
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
        student_num += ap_courses * 1
        student_num += interviewScore * 1.5 # potentially change
        student_num += essayStrength * 2
        student_num += lors * 1
    else:
        # GPA = 35 pts, EC = 15 pts, Essay = 15 pts, AP = 10 pts, Interview = 10 pts, SAT/ACT = 15 pts, lors = 10pts
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
        student_num += interviewScore * 1.5
        student_num += essayStrength * 1
        student_num += lors * 1

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

    print(student_num)
    tier = classify(student_num)
    chances = 0

    if baseChance < 5:  # <5%
        if tier == 1:
            chances = 55 + random.uniform(-2, 2)  # 53-57%
        elif tier == 2:
            chances = 45 + random.uniform(-2, 2)  # 43-47%
        elif tier == 3:
            chances = 33 + random.uniform(-2, 2)  # 31-35%
        elif tier == 4:
            chances = 22 + random.uniform(-2, 2)  # 20-24%
        elif tier == 5:
            chances = 15 + random.uniform(-2, 2)  # 13-17%
        elif tier == 6:
            chances = 9 + random.uniform(-2, 2)   # 7-11%
        elif tier == 7:
            chances = 5 + random.uniform(-2, 2)   # 3-7%
        elif tier == 8:
            chances = 3 + random.uniform(-1, 1)   # 2-4%
        elif tier == 9:
            chances = 2 + random.uniform(-0.5, 0.5)  # 1.5-2.5%
        elif tier == 10:
            chances = 1 + random.uniform(-0.3, 0.3)  # 0.7-1.3%
        elif tier == 11:
            chances = 0.8 + random.uniform(-0.2, 0.2)  # 0.6-1.0%
        elif tier == 12:
            chances = 0.6 + random.uniform(-0.1, 0.1)  # 0.5-0.7%
        elif tier == 13:
            chances = 0.4 + random.uniform(-0.05, 0.05)  # 0.35-0.45%
        elif tier == 14:
            chances = 0.2 + random.uniform(-0.02, 0.02)  # 0.18-0.22%
        elif tier == 15:
            chances = 0.1 + random.uniform(-0.01, 0.01)  # 0.09-0.11%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 10:  # <10%
        if tier == 1:
            chances = 60 + random.uniform(-2, 2)  # 58-62%
        elif tier == 2:
            chances = 48 + random.uniform(-2, 2)  # 46-50%
        elif tier == 3:
            chances = 39 + random.uniform(-2, 2)  # 37-41%
        elif tier == 4:
            chances = 28 + random.uniform(-2, 2)  # 26-30%
        elif tier == 5:
            chances = 21 + random.uniform(-2, 2)  # 19-23%
        elif tier == 6:
            chances = 16 + random.uniform(-2, 2)  # 14-18%
        elif tier == 7:
            chances = 12 + random.uniform(-2, 2)  # 10-14%
        elif tier == 8:
            chances = 7 + random.uniform(-1, 1)   # 6-8%
        elif tier == 9:
            chances = 4 + random.uniform(-0.5, 0.5)  # 3.5-4.5%
        elif tier == 10:
            chances = 2 + random.uniform(-0.3, 0.3)  # 1.7-2.3%
        elif tier == 11:
            chances = 1.5 + random.uniform(-0.1, 0.1)  # 1.4-1.6%
        elif tier == 12:
            chances = 1.2 + random.uniform(-0.05, 0.05)  # 1.15-1.25%
        elif tier == 13:
            chances = 1 + random.uniform(-0.02, 0.02)  # 0.98-1.02%
        elif tier == 14:
            chances = 0.7 + random.uniform(-0.01, 0.01)  # 0.69-0.71%
        elif tier == 15:
            chances = 0.4 + random.uniform(-0.005, 0.005)  # 0.395-0.405%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 15:  # <15%
        if tier == 1:
            chances = 67 + random.uniform(-2, 2)  # 65-69%
        elif tier == 2:
            chances = 55 + random.uniform(-2, 2)  # 53-57%
        elif tier == 3:
            chances = 47 + random.uniform(-2, 2)  # 45-49%
        elif tier == 4:
            chances = 38 + random.uniform(-2, 2)  # 36-40%
        elif tier == 5:
            chances = 29 + random.uniform(-2, 2)  # 27-31%
        elif tier == 6:
            chances = 23 + random.uniform(-2, 2)  # 21-25%
        elif tier == 7:
            chances = 16 + random.uniform(-2, 2)  # 14-18%
        elif tier == 8:
            chances = 10 + random.uniform(-1, 1)   # 9-11%
        elif tier == 9:
            chances = 6 + random.uniform(-0.5, 0.5)  # 5.5-6.5%
        elif tier == 10:
            chances = 4 + random.uniform(-0.3, 0.3)  # 3.7-4.3%
        elif tier == 11:
            chances = 2 + random.uniform(-0.1, 0.1)  # 1.9-2.1%
        elif tier == 12:
            chances = 0.8 + random.uniform(-0.05, 0.05)  # 0.75-0.85%
        elif tier == 13:
            chances = 0.6 + random.uniform(-0.02, 0.02)  # 0.58-0.62%
        elif tier == 14:
            chances = 0.3 + random.uniform(-0.01, 0.01)  # 0.29-0.31%
        elif tier == 15:
            chances = 0.15 + random.uniform(-0.005, 0.005)  # 0.145-0.155%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 20:  # <20%
        if tier == 1:
            chances = 73 + random.uniform(-2, 2)  # 71-75%
        elif tier == 2:
            chances = 63 + random.uniform(-2, 2)  # 61-65%
        elif tier == 3:
            chances = 54 + random.uniform(-2, 2)  # 52-56%
        elif tier == 4:
            chances = 43 + random.uniform(-2, 2)  # 41-45%
        elif tier == 5:
            chances = 35 + random.uniform(-2, 2)  # 33-37%
        elif tier == 6:
            chances = 27 + random.uniform(-2, 2)  # 25-29%
        elif tier == 7:
            chances = 21 + random.uniform(-2, 2)  # 19-23%
        elif tier == 8:
            chances = 15 + random.uniform(-1, 1)   # 14-16%
        elif tier == 9:
            chances = 11 + random.uniform(-0.5, 0.5)  # 10.5-11.5%
        elif tier == 10:
            chances = 7 + random.uniform(-0.3, 0.3)   # 6.7-7.3%
        elif tier == 11:
            chances = 5 + random.uniform(-0.1, 0.1)   # 4.9-5.1%
        elif tier == 12:
            chances = 3 + random.uniform(-0.05, 0.05)  # 2.95-3.05%
        elif tier == 13:
            chances = 0.8 + random.uniform(-0.02, 0.02)  # 0.78-0.82%
        elif tier == 14:
            chances = 0.5 + random.uniform(-0.01, 0.01)  # 0.49-0.51%
        elif tier == 15:
            chances = 0.25 + random.uniform(-0.005, 0.005)  # 0.245-0.255%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 25:  # <25%
        if tier == 1:
            chances = 79 + random.uniform(-2, 2)  # 77-81%
        elif tier == 2:
            chances = 70 + random.uniform(-2, 2)  # 68-72%
        elif tier == 3:
            chances = 60 + random.uniform(-2, 2)  # 58-62%
        elif tier == 4:
            chances = 50 + random.uniform(-2, 2)  # 48-52%
        elif tier == 5:
            chances = 40 + random.uniform(-2, 2)  # 38-42%
        elif tier == 6:
            chances = 33 + random.uniform(-2, 2)  # 31-35%
        elif tier == 7:
            chances = 25 + random.uniform(-2, 2)  # 23-27%
        elif tier == 8:
            chances = 20 + random.uniform(-1, 1)   # 19-21%
        elif tier == 9:
            chances = 16 + random.uniform(-0.5, 0.5)  # 15.5-16.5%
        elif tier == 10:
            chances = 12 + random.uniform(-0.3, 0.3)  # 11.7-12.3%
        elif tier == 11:
            chances = 8 + random.uniform(-0.1, 0.1)   # 7.9-8.1%
        elif tier == 12:
            chances = 5 + random.uniform(-0.05, 0.05)  # 4.95-5.05%
        elif tier == 13:
            chances = 3 + random.uniform(-0.02, 0.02)  # 2.98-3.02%
        elif tier == 14:
            chances = 1 + random.uniform(-0.01, 0.01)  # 0.99-1.01%
        elif tier == 15:
            chances = 0.5 + random.uniform(-0.005, 0.005)  # 0.495-0.505%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 30:  # <30%
        if tier == 1:
            chances = 83 + random.uniform(-2, 2)  # 81-85%
        elif tier == 2:
            chances = 74 + random.uniform(-2, 2)  # 72-76%
        elif tier == 3:
            chances = 66 + random.uniform(-2, 2)  # 64-68%
        elif tier == 4:
            chances = 54 + random.uniform(-2, 2)  # 52-56%
        elif tier == 5:
            chances = 43 + random.uniform(-2, 2)  # 41-45%
        elif tier == 6:
            chances = 35 + random.uniform(-2, 2)  # 33-37%
        elif tier == 7:
            chances = 27 + random.uniform(-2, 2)  # 25-29%
        elif tier == 8:
            chances = 21 + random.uniform(-1, 1)   # 20-22%
        elif tier == 9:
            chances = 18 + random.uniform(-0.5, 0.5)  # 17.5-18.5%
        elif tier == 10:
            chances = 15 + random.uniform(-0.3, 0.3)  # 14.7-15.3%
        elif tier == 11:
            chances = 12 + random.uniform(-0.1, 0.1)   # 11.9-12.1%
        elif tier == 12:
            chances = 10 + random.uniform(-0.05, 0.05)  # 9.95-10.05%
        elif tier == 13:
            chances = 7 + random.uniform(-0.02, 0.02)   # 6.98-7.02%
        elif tier == 14:
            chances = 5 + random.uniform(-0.01, 0.01)   # 4.99-5.01%
        elif tier == 15:
            chances = 1.5 + random.uniform(-0.005, 0.005)  # 1.495-1.505%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 35:  # <35%
        if tier == 1:
            chances = 87 + random.uniform(-2, 2)  # 85-89%
        elif tier == 2:
            chances = 80 + random.uniform(-2, 2)  # 78-82%
        elif tier == 3:
            chances = 73 + random.uniform(-2, 2)  # 71-75%
        elif tier == 4:
            chances = 66 + random.uniform(-2, 2)  # 64-68%
        elif tier == 5:
            chances = 59 + random.uniform(-2, 2)  # 57-61%
        elif tier == 6:
            chances = 52 + random.uniform(-2, 2)  # 50-54%
        elif tier == 7:
            chances = 45 + random.uniform(-2, 2)  # 43-47%
        elif tier == 8:
            chances = 39 + random.uniform(-1, 1)   # 38-40%
        elif tier == 9:
            chances = 36 + random.uniform(-0.5, 0.5)  # 35.5-36.5%
        elif tier == 10:
            chances = 33 + random.uniform(-0.3, 0.3)  # 32.7-33.3%
        elif tier == 11:
            chances = 30 + random.uniform(-0.1, 0.1)   # 29.9-30.1%
        elif tier == 12:
            chances = 28 + random.uniform(-0.05, 0.05)  # 27.95-28.05%
        elif tier == 13:
            chances = 25 + random.uniform(-0.02, 0.02)   # 24.98-25.02%
        elif tier == 14:
            chances = 22 + random.uniform(-0.01, 0.01)   # 21.99-22.01%
        elif tier == 15:
            chances = 19 + random.uniform(-0.005, 0.005)  # 18.995-19.005%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 45:  # <45%
        if tier == 1:
            chances = 90 + random.uniform(-2, 2)  # 88-92%
        elif tier == 2:
            chances = 83 + random.uniform(-2, 2)  # 81-85%
        elif tier == 3:
            chances = 76 + random.uniform(-2, 2)  # 74-78%
        elif tier == 4:
            chances = 69 + random.uniform(-2, 2)  # 67-71%
        elif tier == 5:
            chances = 62 + random.uniform(-2, 2)  # 60-64%
        elif tier == 6:
            chances = 55 + random.uniform(-2, 2)  # 53-57%
        elif tier == 7:
            chances = 48 + random.uniform(-2, 2)  # 46-50%
        elif tier == 8:
            chances = 42 + random.uniform(-1, 1)   # 41-43%
        elif tier == 9:
            chances = 39 + random.uniform(-0.5, 0.5)  # 38.5-39.5%
        elif tier == 10:
            chances = 36 + random.uniform(-0.3, 0.3)  # 35.7-36.3%
        elif tier == 11:
            chances = 33 + random.uniform(-0.1, 0.1)   # 32.9-33.1%
        elif tier == 12:
            chances = 31 + random.uniform(-0.05, 0.05)  # 30.95-31.05%
        elif tier == 13:
            chances = 28 + random.uniform(-0.02, 0.02)   # 27.98-28.02%
        elif tier == 14:
            chances = 25 + random.uniform(-0.01, 0.01)   # 24.99-25.01%
        elif tier == 15:
            chances = 22 + random.uniform(-0.005, 0.005)  # 21.995-22.005%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 60:  # <60%
        if tier == 1:
            chances = 93 + random.uniform(-2, 2)  # 91-95%
        elif tier == 2:
            chances = 86 + random.uniform(-2, 2)  # 84-88%
        elif tier == 3:
            chances = 79 + random.uniform(-2, 2)  # 77-81%
        elif tier == 4:
            chances = 72 + random.uniform(-2, 2)  # 70-74%
        elif tier == 5:
            chances = 62 + random.uniform(-2, 2)  # 63-67%
        elif tier == 6:
            chances = 53 + random.uniform(-2, 2)  # 56-60%
        elif tier == 7:
            chances = 39 + random.uniform(-2, 2)  # 49-53%
        elif tier == 8:
            chances = 33 + random.uniform(-1, 1)   # 44-46%
        elif tier == 9:
            chances = 26 + random.uniform(-0.5, 0.5)  # 41.5-42.5%
        elif tier == 10:
            chances = 22 + random.uniform(-0.3, 0.3)  # 38.7-39.3%
        elif tier == 11:
            chances = 19 + random.uniform(-0.1, 0.1)   # 35.9-36.1%
        elif tier == 12:
            chances = 15 + random.uniform(-0.05, 0.05)  # 33.95-34.05%
        elif tier == 13:
            chances = 12 + random.uniform(-0.02, 0.02)   # 30.98-31.02%
        elif tier == 14:
            chances = 9 + random.uniform(-0.01, 0.01)   # 27.99-28.01%
        elif tier == 15:
            chances = 5 + random.uniform(-0.005, 0.005)  # 24.995-25.005%
        else:
            chances = 0.05  # Default for tiers >15

    elif baseChance < 80:  # <80%
        if tier == 1:
            chances = 94 + random.uniform(-2, 2)  # 95-99%
        elif tier == 2:
            chances = 88 + random.uniform(-2, 2)  # 88-92%
        elif tier == 3:
            chances = 80 + random.uniform(-2, 2)  # 81-85%
        elif tier == 4:
            chances = 74 + random.uniform(-2, 2)  # 74-78%
        elif tier == 5:
            chances = 67 + random.uniform(-2, 2)  # 67-71%
        elif tier == 6:
            chances = 60 + random.uniform(-2, 2)  # 60-64%
        elif tier == 7:
            chances = 53 + random.uniform(-2, 2)  # 53-57%
        elif tier == 8:
            chances = 47 + random.uniform(-1, 1)   # 48-50%
        elif tier == 9:
            chances = 42 + random.uniform(-0.5, 0.5)  # 45.5-46.5%
        elif tier == 10:
            chances = 36 + random.uniform(-0.3, 0.3)  # 42.7-43.3%
        elif tier == 11:
            chances = 29 + random.uniform(-0.1, 0.1)   # 39.9-40.1%
        elif tier == 12:
            chances = 23 + random.uniform(-0.05, 0.05)  # 37.95-38.05%
        elif tier == 13:
            chances = 19 + random.uniform(-0.02, 0.02)   # 34.98-35.02%
        elif tier == 14:
            chances = 15 + random.uniform(-0.01, 0.01)   # 31.99-32.01%
        elif tier == 15:
            chances = 12 + random.uniform(-0.005, 0.005)  # 28.995-29.005%
        else:
            chances = 0.05  # Default for tiers >15

    else:
        # baseChance >=80%
        if tier == 1:
            chances = 97 + random.uniform(-2, 2)  # 95-99%
        elif tier == 2:
            chances = 90 + random.uniform(-2, 2)  # 88-92%
        elif tier == 3:
            chances = 83 + random.uniform(-2, 2)  # 81-85%
        elif tier == 4:
            chances = 76 + random.uniform(-2, 2)  # 74-78%
        elif tier == 5:
            chances = 69 + random.uniform(-2, 2)  # 67-71%
        elif tier == 6:
            chances = 62 + random.uniform(-2, 2)  # 60-64%
        elif tier == 7:
            chances = 55 + random.uniform(-2, 2)  # 53-57%
        elif tier == 8:
            chances = 49 + random.uniform(-1, 1)   # 48-50%
        elif tier == 9:
            chances = 46 + random.uniform(-0.5, 0.5)  # 45.5-46.5%
        elif tier == 10:
            chances = 43 + random.uniform(-0.3, 0.3)  # 42.7-43.3%
        elif tier == 11:
            chances = 40 + random.uniform(-0.1, 0.1)   # 39.9-40.1%
        elif tier == 12:
            chances = 38 + random.uniform(-0.05, 0.05)  # 37.95-38.05%
        elif tier == 13:
            chances = 35 + random.uniform(-0.02, 0.02)   # 34.98-35.02%
        elif tier == 14:
            chances = 32 + random.uniform(-0.01, 0.01)   # 31.99-32.01%
        elif tier == 15:
            chances = 29 + random.uniform(-0.005, 0.005)  # 28.995-29.005%
        else:
            chances = 0.05  # Default for tiers >15
            
    chances = max(0.0, min(chances, 100.0))

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
            
    # home state stuff
    if collegeList[i][0] == "cornell" and state == "NY":
        chances *= random.uniform(1.0, 1.2)  # Cornell prefers NY applicants slightly
    elif collegeList[i][0] == "uva" and state == "VA":
        chances *= random.uniform(1.4, 1.8)  # UVA strongly prefers VA residents
    elif collegeList[i][0] == "gtech" and state == "GA":
        chances *= random.uniform(1.4, 1.8)  # Georgia Tech heavily favors GA residents
    elif collegeList[i][0] == "berkeley" and state == "CA" or collegeList[i][0] == "ucla" and state == "CA":
        chances *= random.uniform(1.3, 1.7)  # UC Berkeley strongly prefers CA residents
    elif collegeList[i][0] == "umich" and state == "MI":
        chances *= random.uniform(1.3, 1.5)  # University of Michigan gives preference to MI residents
    elif collegeList[i][0] == "illini" and state == "IL":
        chances *= random.uniform(1.2, 1.4)  # University of Illinois prefers IL residents
    elif collegeList[i][0] == "utexas" and state == "TX":
        if (gpa > 97.6):
            return 100 #ut auto top 6% of texas get in
        else:
            chances *= random.uniform(1.4, 1.9)  # UT prefers texas residents
    elif collegeList[i][0] == "unc" and state == "NC":
        chances *= random.uniform(1.3, 1.6)  # UNC Chapel Hill heavily favors NC residents
    elif collegeList[i][0] == "bing" and state == "NY":
        chances *= random.uniform(1.3, 1.5)  # Binghamton strongly prefers NY residents
    elif collegeList[i][0] == "buffalo" and state == "NY":
        chances *= random.uniform(1.4, 1.6)  # University at Buffalo strongly favors NY residents
    elif collegeList[i][0] == "purdue" and state == "IN":
        chances *= random.uniform(1.3, 1.6)  # purdue indiana 
        
    if legacy == collegeList[i][0]:
        chances *= random.uniform(1.0, 1.5)

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
                    "university_name": next(
        (u["display_name"] for u in university_list if u["name"].lower() == short_name.lower()),
        short_name.capitalize()
    ),
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
                lors = user_data.get('lors', 0.0)
                gpa = user_data.get('gpa', 0.0)
                state = user_data.get('state', 'NY').upper()
                legacy = user_data.get('legacy', 'None')

                # Recompute chances_val_rd using 'app_type'='RD' and reused interview_strength
                chances_val_rd = chanceCollege(
                    collegeList=college_list,
                    i=idx,
                    demScore=demScore,
                    testOptional=testOptional,
                    sat=int(sat),
                    act=int(act),
                    extracurriculars=float(extracurriculars),
                    ap_courses=int(ap_courses),
                    essayStrength=float(essayStrength),
                    gpa=float(gpa),
                    interviewStrength=interview_strength,  # Reuse the initial interview strength
                    app_type="RD",
                    state=state,
                    legacy=legacy,
                    lors=lors
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
    lors = user_data.get('lors', 0.0)
    gpa = user_data.get('gpa', 0.0)
    state = user_data.get('state', 'NY').upper()
    legacy = user_data.get('legacy', 'None')

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
            extracurriculars=float(extracurriculars),
            ap_courses=int(ap_courses),
            essayStrength=float(essayStrength),
            gpa=float(gpa),
            interviewStrength=interview_score,
            app_type=app_type,
            state=state,
            legacy=legacy,
            lors=lors
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
    session.setdefault('final_results', {})
    
    yourFate = random.random() * 100
    if yourFate >= 100:
        yourFate = 100
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
        if collegeName == "harvard" or collegeName == "georgetown":
            if yourFate < chances:
                decision = "A"
            elif yourFate < chances + 40 + random.random() * 40:
                decision = "D"
            else:
                decision = "R"
        elif collegeName == "yale":
            if yourFate < chances:
                decision = "A"
            elif yourFate < chances + random.random() * 25:
                decision = "D"
            else:
                decision = "R"
        elif yourFate < chances:
            decision = "A"
        elif yourFate < chances + random.random() * 40:
            decision = "D"
        else:
            decision = "R"

    elif appType == "EA":
        if collegeName == "mit" or collegeName == "uchicago":
            if yourFate < chances:
                decision = "A"
            elif yourFate < chances + 50 + random.random() * 50:
                decision = "D"
            else:
                decision = "R"
        elif yourFate < chances:
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
        
    if decision in ["W", "D/W"]:
        final_results = session['final_results']
        schedule_waitlist_resolution(
            college_short_name=collegeName,
            decision_code=decision,
            final_results=final_results,
            decisions_queue_sorted=decisions_queue_sorted,
            university_list=university_list   # <-- IMPORTANT FIX
        )

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

# The `results` Route
@app.route('/advancedsim/results', methods=["GET", "POST"])
@login_required
def results():
    session.pop('college_enrolled', None)
    
    # Retrieve user data from session
    user_data = session.get('advancedsim_data', {"name": "User"})
    name = user_data.get("name", "User")

    # Retrieve applied colleges and simulation results from session
    applied_colleges = session.get('applied_colleges', [])
    final_results     = session.get('final_results', {})
    decisions_queue_sorted = session.get('decisions_queue_sorted', [])
    opened_colleges   = session.get('opened_colleges', [])
    locked_until_opened = session.get('locked_until_opened', {})

    print("DEBUG: Currently opened colleges:", opened_colleges)

    # Simulation state defaults
    if 'current_sim_date' not in session:
        session['current_sim_date'] = "2024-11-01"  # default start date
    if 'simulation_started' not in session:
        session['simulation_started'] = False
    if 'simulation_paused' not in session:
        session['simulation_paused'] = True  # paused until user clicks "Start"

    # Convert current_sim_date to datetime object
    try:
        sim_dt = datetime.strptime(session['current_sim_date'], "%Y-%m-%d")
    except ValueError:
        sim_dt = datetime(2024, 11, 1)  # fallback if parsing fails

    # 1) Build or rebuild the decisions queue if not already done
    if not decisions_queue_sorted:
        new_queue = []
        for college in applied_colleges:
            short_name = college['short_name']
            app_type   = college['app_type'].upper()

            # Find matching entry in college_list
            c_entry = next((c for c in college_list if c[0].lower() == short_name.lower()), None)
            if not c_entry:
                continue

            # Determine release date
            if app_type in ["ED", "REA"]:
                rdate = c_entry[5] if (len(c_entry) > 5 and c_entry[5] != "N") else "2099-01-01"
            elif app_type == "EA":
                rdate = c_entry[6] if (len(c_entry) > 6 and c_entry[6] != "N") else "2099-01-01"
            else:  # RD
                rdate = c_entry[7] if (len(c_entry) > 7 and c_entry[7] != "N") else "2099-01-01"

            unique_id = generate_unique_id(short_name, app_type)

            # Build the decisions_queue entry
            new_queue.append({
                "short_name": short_name.lower(),
                "unique_id": unique_id,
                "display_name": next(
                    (u["display_name"] for u in university_list if u["name"].lower() == short_name.lower()),
                    short_name.capitalize()
                ),
                "university_name": next(
                    (u["display_name"] for u in university_list if u["name"].lower() == short_name.lower()),
                    short_name.capitalize()
                ),
                "app_type": app_type,
                "release_date": rdate,
                "formatted_release_date": format_date(rdate),
                "logo_url": next(
                    (u["logo"] for u in university_list if u["name"].lower() == short_name.lower()),
                    'static/logos/default-logo.jpg'
                )
            })

            # Initialize final_results if not present
            if unique_id not in final_results:
                final_results[unique_id] = {
                    'decision_code': 'R',  # Default to Rejected
                    'app_type': app_type,
                    'release_date': rdate
                }
            else:
                # Ensure final_results has the correct release date
                final_results[unique_id]['release_date'] = rdate

        # Sort new_queue by release date
        try:
            new_queue.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
        except ValueError:
            print("DEBUG: Invalid date format during sorting.")
            pass

        # Update session
        session['decisions_queue_sorted'] = new_queue
        decisions_queue_sorted            = new_queue
        session['final_results']          = final_results
    else:
        # Possibly re-sort if needed
        try:
            decisions_queue_sorted.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
            session['decisions_queue_sorted'] = decisions_queue_sorted
        except ValueError:
            print("DEBUG: Invalid date format encountered during re-sorting.")

    # Clean invalid locks
    valid_locked_until_opened = {}
    for rd_uid, early_uid in locked_until_opened.items():
        if any(dd['unique_id'] == early_uid for dd in decisions_queue_sorted):
            valid_locked_until_opened[rd_uid] = early_uid
        else:
            print(f"Removing invalid lock: '{rd_uid}' behind '{early_uid}'")

    session['locked_until_opened'] = valid_locked_until_opened

    def is_locked(uid):
        # Helper to see if a decision is locked behind another
        locking_uid = locked_until_opened.get(uid)
        if not locking_uid:
            return False
        if locking_uid not in final_results:
            return False
        return locking_uid not in opened_colleges

    # 3) Identify which decisions are visible
    visible_decisions = []
    for decision in decisions_queue_sorted:
        uid  = decision['unique_id']
        code = final_results.get(uid, {}).get('decision_code', 'R')
        app_type = decision['app_type']

         # Handle all waitlist decisions
        if app_type == "WL":
            dt_release = datetime.strptime(decision['release_date'], '%Y-%m-%d')
            if sim_dt >= dt_release:
                visible_decisions.append(decision)
            continue  # Skip to next decision

        # If RD deferral, check lock
        is_rd_deferral = (app_type == "RD" and code.startswith("D/"))
        if is_rd_deferral:
            if not is_locked(uid):
                visible_decisions.append(decision)
            continue

        # Otherwise always visible
        visible_decisions.append(decision)

    # 4) Enrich them with 'is_available'
    enriched_decisions_queue = []
    for dec in visible_decisions:
        dt_release = datetime.strptime(dec['release_date'], '%Y-%m-%d')
        dec_copy   = dec.copy()
        dec_copy['is_available'] = (dt_release <= sim_dt)
        enriched_decisions_queue.append(dec_copy)

    # 5) Build a list of opened decisions for main content
    opened_decisions_list = []
    for uid in opened_colleges:
        dq_item = next((x for x in enriched_decisions_queue if x['unique_id'] == uid), None)
        if not dq_item:
            continue

        short_name  = dq_item['short_name']
        display_dec = final_results.get(uid, {})
        code        = display_dec.get('decision_code', 'R')
        date_str    = display_dec.get('release_date', '2099-01-01')

        # Map codes to user-friendly text
        decision_mapping = {
            "ED":   ("ED Acceptance", "ed-acceptance"),
            "A":    ("Acceptance",    "acceptance"),
            "R":    ("Rejection",     "rejection"),
            "W":    ("Waitlisted",    "waitlist"),
            "D":    ("Deferred",      "deferred"),
            "D/R":  ("Deferred Rejection",  "deferred-rejection"),
            "D/A":  ("Deferred Acceptance", "deferred-acceptance"),
            "D/W":  ("Deferred Waitlist",   "deferred-waitlist"),
            "W/A":  ("Waitlist Accepted",   "waitlist-acceptance"),
            "W/R":  ("Waitlist Rejected",   "waitlist-rejection"),
            "D/W/A": ("Deferred Waitlist Accepted", "deferred-waitlist-acceptance"),
            "D/W/R": ("Deferred Waitlist Rejected", "deferred-waitlist-rejection"),
        }
        display_decision, badge_class = decision_mapping.get(code, ("Unknown", "unknown"))

        # Format release date
        try:
            dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_dt = dt_obj.strftime('%B %d, %Y')
        except ValueError:
            formatted_dt = "Unknown Date"

        # **Key Fix**: pull "uni_name" from dq_item
        # This ensures we can reference `{{ decision.uni_name }}` in the template
        uni_name = dq_item.get('uni_name', short_name.capitalize())

        opened_decisions_list.append({
            "unique_id": uid,
            "short_name": short_name,
            "uni_name": uni_name,   # we store it here
            "display_name": dq_item.get('display_name', "Unknown"),
            "app_type": dq_item['app_type'],
            "decision": display_decision,
            "badge_class": badge_class,
            "release_date": formatted_dt
        })

    # 6) Determine if the simulation is done
    simulation_done = False  # Initialize the flag

    for dec in opened_decisions_list:
        print(dec['decision'].lower())
        if dec['app_type'] == 'ED' and dec['decision'].lower() in ["ed acceptance"]:
            simulation_done = True
            break

    if not simulation_done and len(opened_decisions_list) >= len(decisions_queue_sorted):
        simulation_done = True

    # 7) Final updates
    session['decisions_queue_sorted'] = decisions_queue_sorted
    session['final_results'] = final_results

    # 8) Render final template
    return render_template(
        'results.html',
        name=name,
        decisions_queue=enriched_decisions_queue,  # 'is_available' included
        opened_decisions=opened_decisions_list,
        current_sim_date=sim_dt.strftime("%Y-%m-%d"),
        simulation_started=session['simulation_started'],
        simulation_paused=session['simulation_paused'],
        simulation_done=simulation_done  # Pass the simulation_done flag
    )

# Route to Advance Simulation
@app.route('/advancedsim/results/advance', methods=['POST'])
@login_required
def advance_simulation():
    from datetime import datetime, timedelta

    # Ensure simulation has started
    if 'simulation_started' not in session:
        session['simulation_started'] = False
    if not session['simulation_started']:
        session['simulation_started'] = True

    current_date_str = session.get('current_sim_date', '2024-11-01')
    try:
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    except ValueError:
        current_date = datetime(2024, 11, 1)
        logger.warning(f"Invalid current_sim_date format: {current_date_str}. Resetting to 2024-11-01.")

    decisions_queue_sorted = session.get('decisions_queue_sorted', [])
    opened_colleges = session.get('opened_colleges', [])
    locked_until_opened = session.get('locked_until_opened', {})
    final_results = session.get('final_results', {})

    # 1) Check if user already has an ED acceptance => end the simulation
    #    (We look for code "ED" or app_type == 'ED' with decision_code that indicates acceptance.)
    ed_done = False
    for uid in opened_colleges:
        dec_info = final_results.get(uid, {})
        if dec_info.get('app_type') == 'ED':
            code = dec_info.get('decision_code', '')
            # If code == "ED" or is some acceptance form, we consider that ED acceptance
            # (some folks store "ED" as the decision_code, or "A" with app_type=ED, etc.)
            if code in ["ED", "A", "D/A", "W/A", "D/W/A"]:
                ed_done = True
                break

    if ed_done:
        return jsonify({
            "status": "done",
            "message": "Simulation ended due to Early Decision acceptance.",
            "current_sim_date": session.get('current_sim_date', '2024-11-01'),
            "current_sim_date_formatted": format_date(session.get('current_sim_date', '2024-11-01')),
            "keep_going": False,
            "is_release_date": False
        })

    # 2) Identify future release dates for un-opened, unlocked colleges
    #    (the rest of this logic is the same as your original code)
    last_waitlist_date = datetime(2025, 6, 20)
    future_dates = []
    for d in decisions_queue_sorted:
        uid = d['unique_id']
        if uid in opened_colleges:
            continue
        # If locked behind ED/EA deferral logic:
        if uid in locked_until_opened and locked_until_opened[uid] not in opened_colleges:
            continue
        try:
            rd = datetime.strptime(d['release_date'], '%Y-%m-%d')
        except ValueError:
            rd = datetime(2099, 1, 1)
        if rd > current_date:
            future_dates.append(rd)

    # Check unopened waitlists
    not_opened_waitlists = []
    for uid, info in final_results.items():
        if info.get('app_type') == 'WL' and uid not in opened_colleges:
            try:
                wldate = datetime.strptime(info.get('release_date', '2099-01-01'), '%Y-%m-%d')
            except ValueError:
                wldate = datetime(2099, 1, 1)
            if wldate <= last_waitlist_date:
                not_opened_waitlists.append(uid)

    # If no more future release dates and no unopened WL => done
    if not future_dates and not not_opened_waitlists:
        session['current_sim_date'] = current_date.strftime("%Y-%m-%d")
        session.modified = True
        return jsonify({
            "status": "done",
            "message": "No more decisions left to release.",
            "current_sim_date": session['current_sim_date'],
            "current_sim_date_formatted": format_date(session['current_sim_date']),
            "keep_going": False,
            "is_release_date": False
        })

    # 3) Advance date by one day or clamp to next release date
    next_release_date = min(future_dates) if future_dates else last_waitlist_date
    new_date = current_date + timedelta(days=1)
    reached_release = False
    if new_date >= next_release_date:
        new_date = next_release_date
        reached_release = True

    if new_date > last_waitlist_date:
        new_date = last_waitlist_date
        reached_release = True

    session['current_sim_date'] = new_date.strftime("%Y-%m-%d")
    session.modified = True
    formatted_date = new_date.strftime('%B %d, %Y')

    # Final check if we just clamped to last_waitlist_date
    if new_date >= last_waitlist_date:
        future_dates_after_clamp = []
        not_opened_waitlists_after_clamp = []
        for d in decisions_queue_sorted:
            uid = d['unique_id']
            if uid in opened_colleges:
                continue
            try:
                rd = datetime.strptime(d['release_date'], '%Y-%m-%d')
            except ValueError:
                rd = datetime(2099, 1, 1)
            if rd > new_date:
                future_dates_after_clamp.append(rd)
            if d['app_type'] == 'WL' and rd <= last_waitlist_date:
                not_opened_waitlists_after_clamp.append(uid)

        if not future_dates_after_clamp and not not_opened_waitlists_after_clamp:
            return jsonify({
                "status": "done",
                "message": "No more decisions left to release.",
                "current_sim_date": session['current_sim_date'],
                "current_sim_date_formatted": format_date(session['current_sim_date']),
                "keep_going": False,
                "is_release_date": False
            })

    # Otherwise, normal "ok" response
    return jsonify({
        "status": "ok",
        "current_sim_date": session['current_sim_date'],
        "current_sim_date_formatted": formatted_date,
        "keep_going": (not reached_release),
        "is_release_date": reached_release,
        "message": f"Advanced to {session['current_sim_date']}."
    })
    
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

def schedule_waitlist_resolution(college_short_name, decision_code, final_results, decisions_queue_sorted, university_list):
    """
    Creates a new WL unique_id (waitlist final decision) that will appear in the portal
    at a random date between April 5, 2025 and June 20, 2025, just like any ED/EA/RD release.
    """
    import random
    from datetime import datetime, timedelta

    # This code block assigns a final outcome:
    #   - If currently "W" => 20% chance acceptance => "W/A" or "W/R"
    #   - If currently "D/W" => 20% chance acceptance => "D/W/A" or "D/W/R"
    if random.random() < 0.2:
        final_outcome = f"{decision_code}/A"  # e.g., W/A or D/W/A
    else:
        final_outcome = f"{decision_code}/R"  # e.g., W/R or D/W/R

    # Assign a random date between Apr 5 and June 20, 2025
    start_date = datetime(2025, 4, 5)
    end_date   = datetime(2025, 6, 20)
    delta      = end_date - start_date
    random_days = random.randint(0, delta.days)
    resolution_date = start_date + timedelta(days=random_days)
    release_date_str = resolution_date.strftime("%Y-%m-%d")

    # Generate a unique ID for this waitlist final outcome. 
    # E.g. "brown_wl_1234"
    wl_unique_id = f"{college_short_name.lower()}_wl_{random.randint(1000,9999)}"

    # Store that outcome in final_results so we know the code (W/A, W/R, D/W/A, D/W/R)
    final_results[wl_unique_id] = {
        'decision_code': final_outcome,  # e.g. 'W/A' or 'W/R'
        'app_type': 'WL',               # Distinguish as waitlist resolution
        'release_date': release_date_str
    }

    # **Add** an item in `decisions_queue_sorted` for *any* final outcome, 
    # not just acceptance:
    uni_info = next(
        (u for u in university_list if u["name"].lower() == college_short_name.lower()),
        None
    )
    if uni_info:
        disp_name = f"{uni_info['display_name']} Waitlist Update"
        uni_name  = uni_info['display_name']
        logo_url  = uni_info.get("logo", "static/logos/default-logo.jpg")
    else:
        disp_name = f"{college_short_name.capitalize()} Waitlist Update"
        uni_name  = college_short_name.capitalize()
        logo_url  = "static/logos/default-logo.jpg"

    wl_item = {
        "short_name": college_short_name.lower(),
        "unique_id": wl_unique_id,
        "display_name": disp_name,
        "uni_name": uni_name,
        "app_type": "WL",
        "release_date": release_date_str,
        "formatted_release_date": format_date(release_date_str),
        "logo_url": logo_url,
        # Optionally, you can store is_available = False here, 
        # but the logic in your route sets that at runtime anyway.
    }
    decisions_queue_sorted.append(wl_item)

    # Sort the queue
    try:
        decisions_queue_sorted.sort(key=lambda x: datetime.strptime(x['release_date'], '%Y-%m-%d'))
    except ValueError:
        pass

    session['final_results']            = final_results
    session['decisions_queue_sorted']   = decisions_queue_sorted
    session.modified = True

    print(f"[Waitlist] Scheduled waitlist resolution for {college_short_name.upper()} on {release_date_str} => {final_outcome}")

@app.route('/advancedsim/decision', methods=['GET', 'POST'])
@login_required
def decision():
    # 1) Grab what we need from session
    final_results = session.get('final_results', {})
    opened_colleges = session.get('opened_colleges', [])
    decisions_queue = session.get('decisions_queue_sorted', [])
    college_enrolled = session.get('college_enrolled', None)  # user’s final choice, if any

    # 2) Filter out which colleges are "accepted"
    accepted_offers = []
    for uid in opened_colleges:
        decision_info = final_results.get(uid)
        if not decision_info:
            continue
        decision_code = decision_info.get('decision_code', 'R')

        # Check if it's an acceptance scenario
        if decision_code in ["ED", "EA", "REA", "A", "D/A", "W/A", "D/W/A"]:
            # Look up the matching item in decisions_queue for display_name, short_name, etc.
            dq_item = next((d for d in decisions_queue if d['unique_id'] == uid), None)
            if dq_item:
                short_name = dq_item['short_name'].lower()
                # Find the matching university entry
                uni_info = next((u for u in university_list if u['name'].lower() == short_name), None)

                # Build your accepted_offers object
                accepted_offers.append({
                    "unique_id": uid,
                    "short_name": short_name,
                    "display_name": dq_item.get("display_name", short_name.capitalize()),
                    "university_name": dq_item.get("university_name", short_name.capitalize()),
                    "decision_code": decision_code,
                    "logo_url": uni_info['logo'] if uni_info else "logos/default-logo.jpg",
                    "app_type": dq_item['app_type']
                })

    # 3) Handle POST => user picks which college they want to attend
    if request.method == 'POST':
        chosen_uid = request.form.get('chosen_uid', None)
        if chosen_uid:
            valid_uids = [o["unique_id"] for o in accepted_offers]
            if chosen_uid in valid_uids:
                session['college_enrolled'] = chosen_uid
                session.modified = True
                flash("Congratulations! You have enrolled!", "success")
            else:
                flash("Invalid selection.", "error")
        return redirect(url_for('decision'))

    # 4) If user already enrolled, find that entry
    enrolled_college = None
    if college_enrolled:
        enrolled_college = next((o for o in accepted_offers if o["unique_id"] == college_enrolled), None)

    # 5) Render
    return render_template(
        'decision.html',
        accepted_offers=accepted_offers,
        enrolled_college=enrolled_college
    )

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')  # e.g., December 19, 2024
    except ValueError:
        return "Unknown Date"

# Advanced Simulation Login Route
@app.route("/advancedsim/<college>/login", methods=["GET", "POST"])
def adv_login(college):
    user_data = session.get("advancedsim_data", {"name": "User"})
    unique_id = request.args.get("unique_id")  # Retrieve unique_id from query parameters
    
    if not unique_id:
        # Redirect to results if unique_id is missing
        flash("No unique_id provided. Redirecting to the results page.", "warning")
        return redirect(url_for("results"))

    final_results = session.get("final_results", {})
    decision_info = final_results.get(unique_id, {})
    release_date_str = decision_info.get("release_date", "Unknown Date")
    name = user_data.get("name", "User")

    if request.method == "POST":
        if college.lower() == "utexas" or college.lower() == "ucla":
            decision_code = decision_info.get("decision_code", "R")
            if decision_code in ["A", "ED", "D/A"]:
                return redirect(url_for("adv_acceptance", college=college, unique_id=unique_id))
            elif decision_code in ["D/R"]:
                return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))
            elif decision_code in ["D"]:
                return redirect(url_for("adv_deferred", college=college, unique_id=unique_id))
            elif decision_code in ["D/W", "W"]:
                return redirect(url_for("adv_waitlist", college=college, unique_id=unique_id))
            elif decision_code in ["D/W/A", "W/A"]:
                return redirect(url_for("adv_wacceptance", college=college, unique_id=unique_id))
            elif decision_code in ["D/W/R", "W/R"]:
                return redirect(url_for("adv_wrejection", college=college, unique_id=unique_id))
            else:
                return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))
            
            
        email = request.form.get("email")
        password = request.form.get("password")

        # Simulate authentication (replace with actual logic as needed)
        if not email or not password:
            return render_template(
                f"adv/{college}/login.html",
                error="Please fill out all fields.",
                college=college,
                name=name,
                release_date=release_date_str,
            )

        # Redirect based on the decision code for Northeastern
        if college.lower() == "northeastern" or college.lower() == "utexas" or college.lower() == "ucla":
            decision_code = decision_info.get("decision_code", "R")
            if decision_code in ["A", "ED", "D/A"]:
                return redirect(url_for("adv_acceptance", college=college, unique_id=unique_id))
            elif decision_code in ["R", "D/R"]:
                return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))
            elif decision_code in ["D"]:
                return redirect(url_for("adv_deferred", college=college, unique_id=unique_id))
            elif decision_code in ["D/W", "W"]:
                return redirect(url_for("adv_waitlist", college=college, unique_id=unique_id))
            elif decision_code in ["D/W/A", "W/A"]:
                return redirect(url_for("adv_wacceptance", college=college, unique_id=unique_id))
            elif decision_code in ["D/W/R", "W/R"]:
                return redirect(url_for("adv_wrejection", college=college, unique_id=unique_id))
            else:
                return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))
        
        # For other colleges, redirect to ustatus
        return redirect(url_for("adv_ustatus", college=college, unique_id=unique_id))

    # Render login page for GET request
    return render_template(
        f"adv/{college}/login.html",
        name=name,
        college=college,
        release_date=release_date_str,
    )

@app.route("/advancedsim/<college>/ustatus", methods=["GET", "POST"])
@login_required
def adv_ustatus(college):
    user_data = session.get("advancedsim_data", {"name": "User", "date": "N/A"})
    final_results = session.get("final_results", {})
    
    # Retrieve unique_id from query parameters or form data
    unique_id = request.args.get("unique_id") or request.form.get("unique_id")
    if not unique_id:
        flash("Welcome back to your results page!", "info")
        return redirect(url_for("results"))

    # Get information for the provided unique_id
    info = final_results.get(unique_id)
    if not info:
        flash(f"No record found for {unique_id}.", "danger")
        return redirect(url_for("results"))

    decision_code = info.get("decision_code", "R")
    release_date_str = info.get("release_date", "Unknown Date")

    # Format the release date
    try:
        dt = datetime.strptime(release_date_str, "%Y-%m-%d")
        formatted_date = dt.strftime("%B %d, %Y")
    except ValueError:
        formatted_date = "Unknown Date"

    name = user_data.get("name", "User")

    if request.method == "POST":
        # Mark the college as opened
        if "read_emails" not in session:
            session["read_emails"] = {}
        session["read_emails"][college.lower()] = True
        session.modified = True

        # Redirect based on the decision code
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
        elif decision_code in ["D/W", "W"]:
            return redirect(url_for("adv_waitlist", college=college, unique_id=unique_id))
        elif decision_code in ["D/W/A", "W/A"]:
            return redirect(url_for("adv_wacceptance", college=college, unique_id=unique_id))
        elif decision_code in ["D/W/R", "W/R"]:
            return redirect(url_for("adv_wrejection", college=college, unique_id=unique_id))
        else:
            return redirect(url_for("adv_rejection", college=college, unique_id=unique_id))

    # Determine which template to render
    if college.lower() == "umich" and decision_code == "D":
        template_name = f"adv/{college}/d_ustatus.html"
    else:
        template_name = f"adv/{college}/ustatus.html"

    # Render the appropriate status page for GET request
    return render_template(
        template_name,
        name=name,
        college=college,
        date=formatted_date,
        decision_code=decision_code,
        unique_id=unique_id,  # Ensure unique_id is passed to the template
    )
    
@app.context_processor
def inject_formatted_date():
    def format_date(date_str):
        try:
            # Parse the original date string
            parsed_date = datetime.strptime(date_str, '%B %d, %Y')
            # Format to desired output: mm/dd/yy
            return parsed_date.strftime('%m/%d/%y')
        except ValueError:
            # If parsing fails, return the original string
            return date_str
    return dict(format_date=format_date)

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
    
@app.route("/advancedsim/<college>/wacceptance")
@login_required
def adv_wacceptance(college):
    unique_id = request.args.get('unique_id')
    if not unique_id:
        flash("No unique_id provided for waitlist acceptance.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    info = final_results.get(unique_id)
    if not info:
        flash("Waitlist acceptance record not found.", "danger")
        return redirect(url_for('results'))

    release_date_str = info.get('release_date', 'Unknown Date')
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    # Log or track user action
    user_id = session.get('user_id')
    if user_id:
        User.log_simulation(user_id, college, 'wacceptance')

    name = session.get("advancedsim_data", {}).get("name", "User")
    return render_template(
        f"adv/{college}/wacceptance.html",
        name=name,
        date=formatted_date,
        college=college
    )

@app.route("/advancedsim/<college>/wrejection")
@login_required
def adv_wrejection(college):
    unique_id = request.args.get('unique_id')
    if not unique_id:
        flash("No unique_id provided for waitlist rejection.", "danger")
        return redirect(url_for('results'))

    final_results = session.get('final_results', {})
    info = final_results.get(unique_id)
    if not info:
        flash("Waitlist rejection record not found.", "danger")
        return redirect(url_for('results'))

    release_date_str = info.get('release_date', 'Unknown Date')
    try:
        dt = datetime.strptime(release_date_str, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except ValueError:
        formatted_date = "Unknown Date"

    user_id = session.get('user_id')
    if user_id:
        User.log_simulation(user_id, college, 'wrejection')

    name = session.get("advancedsim_data", {}).get("name", "User")
    return render_template(
        f"adv/{college}/wrejection.html",
        name=name,
        date=formatted_date,
        college=college
    )


@app.route('/advancedsim/mark_as_read', methods=['POST'])
@login_required
def mark_as_read():
    data = request.get_json()
    uid = data.get('uid', '').lower()

    if not uid:
        return jsonify({"status": "error", "message": "No UID provided."}), 400

    # Add to opened_colleges
    opened_colleges = session.get('opened_colleges', [])
    if uid not in opened_colleges:
        opened_colleges.append(uid)
        session['opened_colleges'] = opened_colleges
        session.modified = True

    return jsonify({"status": "success", "message": "Decision marked as read."}), 200

@app.route('/quicksim/<college>/login_files/<path:filename>')
def login_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'login_files'), filename)

@app.route('/quicksim/<college>/ustatus_files/<path:filename>')
def ustatus_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'ustatus_files'), filename)

@app.route('/quicksim/<college>/acceptance_files/<path:filename>')
def acceptance_files_static(college, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', college, 'acceptance_files'), filename)

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

# Error Handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Page Not Found'), 404

# Error Handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Server Error'), 500

if __name__ == "__main__":
    app.run(debug=True)