import os
import sqlite3 as SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from jinja2 import Environment, PackageLoader, select_autoescape
import datetime
from flask_mail import Mail, Message
from helpers import apology, login_required, sendemail



# Configure application
app = Flask(__name__)
app.app_context().push()

# set configuration and instantiate mail
mail_settings = {

    "MAIL_SERVER": 'smtp.office365.com',

    "MAIL_PORT": 587,

    "MAIL_USE_TLS": True,

    "MAIL_USE_SSL": False,

    "MAIL_USERNAME": 'educafee@outlook.com',

    "MAIL_PASSWORD": 'MartinAdnan'

}

app.config.update(mail_settings)

mail = Mail(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "abc"
Session(app)
db = SQL.connect("educafewebdb.db", check_same_thread = False)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        
        db.execute("UPDATE professors SET role = :role, picture = :picture, linkedin = :linkedin WHERE id = :user_id", role = request.form.get("role"), picture = request.files("picture"), linkedin = request.form.get("linkedin"), user_id = session["user_id"])

        return render_template("home.html")
    else:
        return render_template("myprofile.html")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
#student must be logged in to view
##@login_required
def index():
    return render_template("index.html")


@app.route("/student_register", methods=["GET", "POST"])
def student_register():
    """Register user"""

    # If request method is GET, then user should be directed to register.html (registration page)
    if request.method == "GET":
        return render_template("student_register.html")

    # If request method is POST, then user submitted registration form
    else:
        # Check that username was successfully submitted
        if not request.form.get("username"):
            return apology("Please enter a valid username", 400)

        # Check that username is not blank
        if len(request.form.get("username")) == 0:
            return apology("Please enter a valid username", 400)

        # Check that password was successfully submitted
        if not request.form.get("password"):
            return apology("Please enter a valid password", 400)

        # Check that password is not blank
        if len(request.form.get("password")) == 0:
            return apology("Please enter a valid password", 400)

        # Ensure that the password submitted is greater than 8 characters in length
        if len(request.form.get("password")) < 8:
            return apology("Enter a password that is at least 8 characters long", 400)
        number_present = False
        alphabetical_present = False
        # Make sure alphabetical and numerical characters are present
        for c in request.form.get("password"):
            if c.isdigit():
                number_present = True
            if c.isalpha():
                alphabetical_present = True
        if not number_present:
            return apology("Password must contain at least one numerical character!", 400)
        if not alphabetical_present:
            return apology("Password must contain at least one alphabetical character!", 400)
        # Check that password confirmation was successfully submitted
        if not request.form.get("confirmation"):
            return apology("Please enter a valid confirmation of password", 400)

        # Check that password and confirmation match
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("Confirmation and password do not match", 400)

        # Username query database
        rows = db.execute("SELECT * FROM students WHERE username = ?;", [request.form.get("username")])
        rows = rows.fetchall()
        result = [
                idx for idx, tup in enumerate(rows) if tup[7] == request.form.get("username")
        ]
        print(len(result))

        # Check that username isn't already taken
        if len(result) != 0:
            return apology("username already exists, select other username", 400)
        

        # Add username and password (hash value) to SQL database
        db.execute("INSERT INTO students (email, name, class_year, major, resco, bio, username, hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                   (request.form.get("email"), request.form.get("fullname"), request.form.get("classyear"), request.form.get("major"), 
                   request.form.get("resco"), request.form.get("bio"), request.form.get("username"), generate_password_hash(request.form.get("password"))))

        rows = db.execute("SELECT * FROM students WHERE username = ?;", [request.form.get("username")])
        rows = rows.fetchall()

        result = [
                idx for idx, tup in enumerate(rows) if tup[7] == request.form.get("username")
        ]
        for i in range(len(rows[result[0]])):
            print(rows[result[0]][i])
        session["user_id"] = rows[result[0]][0]

        # Direct user to homepage
        return redirect("/swipes")

@app.route("/prof_register", methods=["GET", "POST"])
def prof_register():
    """Register user"""

    # If request method is GET, then user should be directed to register.html (registration page)
    if request.method == "GET":
        return render_template("prof_register.html")

    # If request method is POST, then user submitted registration form
    else:
        # Check that username was successfully submitted
        if not request.form.get("username"):
            return apology("Please enter a valid username", 400)

        # Check that username is not blank
        if len(request.form.get("username")) == 0:
            return apology("Please enter a valid username", 400)

        # Check that password was successfully submitted
        if not request.form.get("password"):
            return apology("Please enter a valid password", 400)

        # Check that password is not blank
        if len(request.form.get("password")) == 0:
            return apology("Please enter a valid password", 400)

        # Ensure that the password submitted is greater than 8 characters in length
        if len(request.form.get("password")) < 8:
            return apology("Enter a password that is at least 8 characters long", 400)
        number_present = False
        alphabetical_present = False
        # Make sure alphabetical and numerical characters are present
        for c in request.form.get("password"):
            if c.isdigit():
                number_present = True
            if c.isalpha():
                alphabetical_present = True
        if not number_present:
            return apology("Password must contain at least one numerical character!", 400)
        if not alphabetical_present:
            return apology("Password must contain at least one alphabetical character!", 400)
        # Check that password confirmation was successfully submitted
        if not request.form.get("confirmation"):
            return apology("Please enter a valid confirmation of password", 400)

        # Check that password and confirmation match
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("Confirmation and password do not match", 400)

        # Username query database
        rows = db.execute("SELECT * FROM professors WHERE username = ?", [request.form.get("username")])
        rows = rows.fetchall()
        result = [
                idx for idx, tup in enumerate(rows) if tup[5] == request.form.get("username")
        ]
        print(len(result))

        # Check that username isn't already taken
        if len(result) != 0:
            return apology("username already exists, select other username", 400)
        

        # Add username and password (hash value) to SQL database
        db.execute("INSERT INTO professors (email, name, research_field, bio, username, hash, profile) VALUES (?, ?, ?, ?, ?, ?, ?);",
                   (request.form.get("email"), request.form.get("fullname"), request.form.get("research_field"), request.form.get("bio"), 
                   request.form.get("username"), generate_password_hash(request.form.get("password")), request.form.get("profile")))

        rows = db.execute("SELECT * FROM professors WHERE username = ?;", [request.form.get("username")])
        rows = rows.fetchall()

        result = [
                idx for idx, tup in enumerate(rows) if tup[5] == request.form.get("username")
        ]
        for i in range(len(rows[result[0]])):
            print(rows[result[0]][i])
        session["user_id"] = rows[result[0]][0]

        # Direct professor to professor homepage
        return redirect("/prof_welcome")


@app.route("/login", methods=["POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

            

        # Query database for username
        studentrows = db.execute("SELECT * FROM students WHERE username = ?", [request.form.get("username")])
        profrows = db.execute("SELECT * FROM professors WHERE username = ?", [request.form.get("username")])

        studentrows = studentrows.fetchall()
        student_result = [
                idx for idx, tup in enumerate(studentrows) if tup[7] == request.form.get("username")
        ]

        profrows = profrows.fetchall()
        prof_result = [
                idx for idx, tup in enumerate(profrows) if tup[5] == request.form.get("username")
        ]

        # Ensure username exists and password is correct
        if len(student_result) != 1:
            if len(prof_result) != 1:
                return apology("invalid username", 403)
            else:
                if not check_password_hash(profrows[prof_result[0]][6], request.form.get("password")):
                    return apology("invalid password", 403)
                else:
                    session["user_id"] = profrows[prof_result[0]][0]
                    return redirect("/prof_welcome")
        else: 
            if not check_password_hash(studentrows[student_result[0]][8], request.form.get("password")):
                return apology("invalid password", 403)
            else:
                session["user_id"] = studentrows[student_result[0]][0]
                return redirect("/swipes")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/initial_register", methods=["POST"])
def initial_register():
    email = request.form.get("email")
    if "@yale.edu" in email:
        if request.form.get("status") == "student":
            return render_template("student_register.html", yale_email = email)
        elif request.form.get("status") == "professor":
            return render_template("prof_register.html", yale_email = email)
        else: 
            return render_template("Yale.html")
    else:
        return render_template("Yale.html")

@app.route("/initial_login", methods=["POST"])
def initial_login():
    return render_template("login.html")

@app.route("/post_verified", methods=["POST"])
def post_verified():
    return render_template("prof-welcome.html")

@app.route("/prof_post", methods=["GET", "POST"])
def prof_post():
    if request.method == "GET":
        return render_template("prof-post.html")
    if request.method == "POST":
        db.execute("INSERT INTO edumeets (prof_id, location, date, topic, capacity) VALUES (?, ?, ?, ?, ?);",
                   (session["user_id"], request.form.get("location"), request.form.get("date"), request.form.get("topic"), request.form.get("capacity")))
        testrows = db.execute("SELECT * FROM edumeets WHERE location = ?", [request.form.get("location")])
        print(testrows.fetchall())
        profrows = db.execute("SELECT * FROM professors WHERE prof_id = ?", [session["user_id"]])
        profrows = profrows.fetchall()
        prof_result = [
                idx for idx, tup in enumerate(profrows)
        ]
        profname = profrows[prof_result[0]][2]
        profile = profrows[prof_result[0]][7]
        return render_template("prof-post-2.html", name = profname, profile = profile, location = request.form.get("location"), date = request.form.get("date"), topic = request.form.get("topic"))
        

@app.route("/prof_welcome", methods=["GET","POST"])
def prof_welcome():
    #If GET, render professor welcome homepage
    if request.method == "GET":
        return render_template("prof-welcome.html")
    
@app.route("/swipes", methods=["GET","POST"])
def swipes():
    #If GET, render professor welcome homepage
    if request.method == "GET":
        #need to pass in non-swiped edumeets to template 
        edumeets = db.execute("SELECT * FROM edumeets WHERE edumeet_id NOT IN (SELECT edumeet_id FROM swipes)")
        edumeets = edumeets.fetchall()
        edumeet_result = list([
                idx for idx, tup in enumerate(edumeets)
        ])
        profrows = db.execute("SELECT * FROM professors")
        profrows = profrows.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(profrows)
        ])
        profs = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profs.append(profrows[prof_result[j]][2])
                    break

        profphotos = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profphotos.append(profrows[prof_result[j]][7])
                    break

        profbios = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profbios.append(profrows[prof_result[j]][4])
                    break

        edumeets = [list(ele) for ele in edumeets]

        return render_template("swipes.html", edumeets = edumeets, edumeet_result = edumeet_result, profs = profs, profphotos = profphotos, profbios = profbios)

@app.route("/swipe_right", methods=["GET","POST"])
def swipe_right():
    #If POST, user has swiped right
    if request.method == "POST":
        #need to modify most recent edumeet in database and rerender
        db.execute("INSERT INTO swipes (edumeet_id, student_id, is_interested) VALUES (?, ?, ?);",
                   (request.form.get("edumeet_id"), session["user_id"], 1))

        all_edumeets = db.execute("SELECT * FROM edumeets")
        all_edumeets = all_edumeets.fetchall()
        all_edumeets_result = list([
                idx for idx, tup in enumerate(all_edumeets)
        ])

        profrows = db.execute("SELECT * FROM professors")
        profrows = profrows.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(profrows)
        ])
        all_profs = []
        for i in range(len(all_edumeets)):
            for j in range(len(profrows)):
                if (all_edumeets[all_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    all_profs.append(profrows[prof_result[j]][2])
                    break

        all_profs_photos = []
        for i in range(len(all_edumeets)):
            for j in range(len(profrows)):
                if (all_edumeets[all_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    all_profs_photos.append(profrows[prof_result[j]][7])
                    break

        edumeets = db.execute("SELECT * FROM edumeets WHERE edumeet_id NOT IN (SELECT edumeet_id FROM swipes)")
        edumeets = edumeets.fetchall()
        edumeet_result = list([
                idx for idx, tup in enumerate(edumeets)
        ])
        profs = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profs.append(profrows[prof_result[j]][2])
                    break

        profphotos = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profphotos.append(profrows[prof_result[j]][7])
                    break

        profbios = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profbios.append(profrows[prof_result[j]][4])
                    break

        edumeets = [list(ele) for ele in edumeets]

        recipient = db.execute("SELECT * from students WHERE student_id = ?", [session["user_id"]])
        recipient = recipient.fetchall()
        recipient_result = list([
                idx for idx, tup in enumerate(recipient)
        ])
        recipient = recipient[recipient_result[0]][1]

        # create message

        curredumeet = db.execute("SELECT * from edumeets WHERE edumeet_id = ?", [request.form.get("edumeet_id")])
        curredumeet = curredumeet.fetchall()
        curredumeet_result = list([
                idx for idx, tup in enumerate(curredumeet)
        ])
        location = curredumeet[curredumeet_result[0]][2]
        date = curredumeet[curredumeet_result[0]][3]
        
        profname = ""
        for i in range(len(curredumeet)):
            for j in range(len(profrows)):
                if (curredumeet[curredumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profname = profrows[prof_result[j]][2]
                    break
                break

        msg = Message(subject="You are signed up for an EduMeet!",

                    sender="educafee@outlook.com",

                    recipients=[recipient],

                    html=sendemail(location, date, profname))


        msg.msgId = msg.msgId.split('@')[0] + '@short_string'

        mail.send(msg)

        if int(request.form.get("counter")) >= len(edumeets) - 1:
            return redirect("/all_edumeets")
        else:
            return redirect("/swipes")


@app.route("/swipe_left", methods=["GET","POST"])
def swipe_left():
     #If POST, user has swiped right
    if request.method == "POST":
        #need to modify most recent edumeet in database and rerender
        db.execute("INSERT INTO swipes (edumeet_id, student_id, is_interested) VALUES (?, ?, ?);",
                   (request.form.get("edumeet_id"), session["user_id"], 0))

        all_edumeets = db.execute("SELECT * FROM edumeets")
        all_edumeets = all_edumeets.fetchall()
        all_edumeets_result = list([
                idx for idx, tup in enumerate(all_edumeets)
        ])

        profrows = db.execute("SELECT * FROM professors")
        profrows = profrows.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(profrows)
        ])
        all_profs = []
        for i in range(len(all_edumeets)):
            for j in range(len(profrows)):
                if (all_edumeets[all_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    all_profs.append(profrows[prof_result[j]][2])
                    break

        all_profs_photos = []
        for i in range(len(all_edumeets)):
            for j in range(len(profrows)):
                if (all_edumeets[all_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    all_profs_photos.append(profrows[prof_result[j]][7])
                    break

        edumeets = db.execute("SELECT * FROM edumeets WHERE edumeet_id NOT IN (SELECT edumeet_id FROM swipes)")
        edumeets = edumeets.fetchall()
        edumeet_result = list([
                idx for idx, tup in enumerate(edumeets)
        ])
        profs = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profs.append(profrows[prof_result[j]][2])
                    break

        profphotos = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profphotos.append(profrows[prof_result[j]][7])
                    break

        profbios = []
        for i in range(len(edumeets)):
            for j in range(len(profrows)):
                if (edumeets[edumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profbios.append(profrows[prof_result[j]][4])
                    break

        edumeets = [list(ele) for ele in edumeets]

        if int(request.form.get("counter")) >= len(edumeets) - 1:
            return redirect("/all_edumeets")
        else:
            return redirect("/swipes")

@app.route("/verify_post", methods=["GET","POST"])
def verify_post():
    #If GET, render professor welcome homepage
    if request.method == "GET":
        return render_template("prof-post-2.html")

@app.route("/all_edumeets", methods=["GET","POST"])
def all_edumeets():
    #If GET, render professor welcome homepage
    if request.method == "GET":
        #need to modify most recent edumeet in database and rerender
        all_edumeets = db.execute("SELECT * FROM edumeets")
        all_edumeets = all_edumeets.fetchall()
        all_edumeets_result = list([
                idx for idx, tup in enumerate(all_edumeets)
        ])
        my_edumeets = db.execute("SELECT * FROM edumeets INNER JOIN swipes ON edumeets.edumeet_id=swipes.edumeet_id WHERE swipes.is_interested = 1")
        my_edumeets = my_edumeets.fetchall()
        my_edumeets_result = list([
                idx for idx, tup in enumerate(my_edumeets)
        ])

        registered = []
        for i in range(len(all_edumeets)):
            for j in range(len(my_edumeets)):
                if (all_edumeets[all_edumeets_result[i]][0] == my_edumeets[my_edumeets_result[j]][0]):
                    registered.append(all_edumeets[all_edumeets_result[i]][0])
                    break

        profrows = db.execute("SELECT * FROM professors")
        profrows = profrows.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(profrows)
        ])
        all_profs = []
        for i in range(len(all_edumeets)):
            for j in range(len(profrows)):
                if (all_edumeets[all_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    all_profs.append(profrows[prof_result[j]][2])
                    break

        all_profs_photos = []
        for i in range(len(all_edumeets)):
            for j in range(len(profrows)):
                if (all_edumeets[all_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    all_profs_photos.append(profrows[prof_result[j]][7])
                    break

        allprofbios = []
        for i in range(len(all_edumeets)):
            for j in range(len(profrows)):
                if (all_edumeets[all_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    allprofbios.append(profrows[prof_result[j]][4])
                    break
        
        return render_template("all-edumeets.html", all_edumeets = all_edumeets, all_edumeets_result = all_edumeets_result, all_profs = all_profs, all_profs_photos = all_profs_photos, registered = registered)


@app.route("/my_edumeets", methods=["GET","POST"])
def my_edumeets():
    #If GET, render professor welcome homepage
    if request.method == "GET":
        #need to modify most recent edumeet in database and rerender
        my_edumeets = db.execute("SELECT * FROM edumeets INNER JOIN swipes ON edumeets.edumeet_id=swipes.edumeet_id WHERE swipes.is_interested = 1")
        my_edumeets = my_edumeets.fetchall()
        my_edumeets_result = list([
                idx for idx, tup in enumerate(my_edumeets)
        ])

        profrows = db.execute("SELECT * FROM professors")
        profrows = profrows.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(profrows)
        ])
        my_profs = []
        for i in range(len(my_edumeets)):
            for j in range(len(profrows)):
                if (my_edumeets[my_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    my_profs.append(profrows[prof_result[j]][2])
                    break

        my_profs_photos = []
        for i in range(len(my_edumeets)):
            for j in range(len(profrows)):
                if (my_edumeets[my_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    my_profs_photos.append(profrows[prof_result[j]][7])
                    break

        myprofbios = []
        for i in range(len(my_edumeets)):
            for j in range(len(profrows)):
                if (my_edumeets[my_edumeets_result[i]][1] == profrows[prof_result[j]][0]):
                    myprofbios.append(profrows[prof_result[j]][4])
                    break
        
        return render_template("my-edumeets.html", my_edumeets = my_edumeets, my_edumeets_result = my_edumeets_result, my_profs = my_profs, my_profs_photos = my_profs_photos)

@app.route("/load_edumeet", methods=["GET","POST"])
def load_edumeet():
    #If GET, render professor welcome homepage
    if request.method == "POST":
        #need to modify most recent edumeet in database and rerender
        curredumeet = db.execute("SELECT * from edumeets WHERE edumeet_id = ?", [request.form.get("edumeet_id")])
        curredumeet = curredumeet.fetchall()
        curredumeet_result = list([
                idx for idx, tup in enumerate(curredumeet)
        ])

        location = curredumeet[curredumeet_result[0]][2]
        date = curredumeet[curredumeet_result[0]][3]
        topic = curredumeet[curredumeet_result[0]][4]
        id = curredumeet[curredumeet_result[0]][0]

        profrows = db.execute("SELECT * FROM professors")
        profrows = profrows.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(profrows)
        ])
        
        profname = ""
        for i in range(len(curredumeet)):
            for j in range(len(profrows)):
                if (curredumeet[curredumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profname = profrows[prof_result[j]][2]
                    break
                break

        profphoto = ""
        for i in range(len(curredumeet)):
            for j in range(len(profrows)):
                if (curredumeet[curredumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profphoto = profrows[prof_result[j]][7]
                    break
                break

        profbio = ""
        for i in range(len(curredumeet)):
            for j in range(len(profrows)):
                if (curredumeet[curredumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profbio = profrows[prof_result[j]][4]
                    break
                break

        return render_template("not-registered-edumeet.html", location = location, date = date, name = profname, topic = topic, profile = profphoto, bio = profbio, id = id)
    
@app.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        db.execute("INSERT INTO swipes (edumeet_id, student_id, is_interested) VALUES (?, ?, ?);",
                   (request.form.get("edumeet_id"), session["user_id"], 1))
        
        profrows = db.execute("SELECT * FROM professors")
        profrows = profrows.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(profrows)
        ])

        recipient = db.execute("SELECT * from students WHERE student_id = ?", [session["user_id"]])
        recipient = recipient.fetchall()
        recipient_result = list([
                idx for idx, tup in enumerate(recipient)
        ])
        recipient = recipient[recipient_result[0]][1]

        # create message

        curredumeet = db.execute("SELECT * from edumeets WHERE edumeet_id = ?", [request.form.get("edumeet_id")])
        curredumeet = curredumeet.fetchall()
        curredumeet_result = list([
                idx for idx, tup in enumerate(curredumeet)
        ])
        location = curredumeet[curredumeet_result[0]][2]
        date = curredumeet[curredumeet_result[0]][3]
        
        profname = ""
        for i in range(len(curredumeet)):
            for j in range(len(profrows)):
                if (curredumeet[curredumeet_result[i]][1] == profrows[prof_result[j]][0]):
                    profname = profrows[prof_result[j]][2]
                    break
                break

        msg = Message(subject="You are signed up for an EduMeet!",

                    sender="educafee@outlook.com",

                    recipients=[recipient],

                    html=sendemail(location, date, profname))


        msg.msgId = msg.msgId.split('@')[0] + '@short_string'

        mail.send(msg)

        return redirect("/my_edumeets")

@app.route("/student_profile", methods=["GET","POST"])
def student_profile():
    if request.method == "GET":
        return render_template("student-account-info.html")

@app.route("/teacher_profile", methods=["GET","POST"])
def teacher_profile():
    if request.method == "GET":
        return render_template("prof-account-info.html")

@app.route("/prof_my_edumeets", methods=["GET", "POST"])
def prof_my_edumeets():
     #If GET, render professor welcome homepage
    if request.method == "GET":
        #need to modify most recent edumeet in database and rerender
        prof = db.execute("SELECT * FROM professors WHERE prof_id = ?", [session["user_id"]])
        prof = prof.fetchall()
        prof_result = list([
                idx for idx, tup in enumerate(prof)
        ])
        profname = prof[prof_result[0]][2]
        profphoto = prof[prof_result[0]][7]

        all_my_edumeets = db.execute("SELECT * FROM edumeets WHERE prof_id = ?", [session["user_id"]])
        all_my_edumeets = all_my_edumeets.fetchall()
        all__my_edumeets_result = list([
                idx for idx, tup in enumerate(all_my_edumeets)
        ])

        return render_template("prof-my-edumeets.html", my_edumeets = all_my_edumeets, my_edumeets_result = all__my_edumeets_result, profname = profname, photo = profphoto)

if __name__ == '__main__':
    app.debug = True
    app.run()

