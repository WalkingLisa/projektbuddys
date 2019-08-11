from flask import Flask, render_template,request, redirect, url_for
from models import User, db

app=Flask(__name__)#MODEL
db.create_all()

@app.route("/", methods=["GET"])#CONTROLLER
def index():
    return render_template("index.html")#VIEW

@app.route("/blog", methods=["GET"])#CONTROLLER
def blog():
    return render_template("blog.html")#VIEW


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        login_name = request.form.get("login-name")
        login_email = request.form.get("login-email")
        login_password = request.form.get("login-password")

        # create a User object
        user = User(name=login_name, email=login_email, password=login_password)

        # save the user object into a database
        db.add(user)
        db.commit()



        print(login_name)
        print(login_email)
        print(login_password)


        return render_template("loginsuccess.html", user=user)


if __name__ == '__main__':
    app.run(debug=True)