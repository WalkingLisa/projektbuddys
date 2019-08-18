from flask import Flask, render_template,request, redirect, url_for, make_response
from models import User, db
import hashlib
import uuid


app=Flask(__name__)#MODEL
db.create_all()

@app.route("/", methods=["GET"])#CONTROLLER
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/blog", methods=["GET"])#CONTROLLER
def blog():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None

    return render_template("blog.html", user=user)#VIEW


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        login_name = request.form.get("login-name")
        login_email = request.form.get("login-email")
        login_password = request.form.get("login-password")

        hashed_password = hashlib.sha256(login_password.encode()).hexdigest()

        user = db.query(User).filter_by(email=login_email).first()

        if not user:# create a User object
            user = User(name=login_name, email=login_email, password=hashed_password)
        # save the user object into a database
            db.add(user)
            db.commit()

        if hashed_password != user.password:
            return "Das ist leider das falsche Passwort, bitte versuche es erneut."

        elif hashed_password == user.password:
            # create a random session token for this user
            session_token = str(uuid.uuid4())

            # save the session token in a database
            user.session_token = session_token
            db.add(user)
            db.commit()

            # save user's session token into a cookie
            response = make_response(redirect(url_for('index')))
            response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

            return render_template("loginsuccess.html", user=user)

#@app.route("/anmelden", methods=["GET", "POST"])
#def anmelden():
   # if request.method == "GET":
   #     return render_template("anmelden.html")
  #  elif request.method == "POST":
    #    login_name = request.form.get("login-name")
   #     login_password = request.form.get("login-password1")


  #      user = User.fetch_one(query=["login-name", "==", login_name])


        # check if password is incorrect
   #     if login_password != user.password1:
   #         return "Das Passwort ist nicht korrekt. Bitte versuche es erneut."



    #    return render_template("loginsuccess.html", user=user)


if __name__ == '__main__':
    app.run(debug=True)