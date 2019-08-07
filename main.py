from flask import Flask, render_template

app=Flask(__name__)#MODEL

@app.route("/")#CONTROLLER
def index():
    return render_template("index.html")#VIEW

@app.route("/blog")#CONTROLLER
def blog():
    return render_template("blog.html")#VIEW

if __name__ == '__main__':
    app.run()