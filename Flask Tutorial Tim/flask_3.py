
import email

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "sdasdsfgsd"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)


# Database

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email



@app.route("/")
def home():
    return render_template("index.html")




@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent  = True
        user = request.form["nm"]
        session["user"] = user
        flash( "Login succesful")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash ("Alredy loge in")
            return redirect(url_for("user"))

        return render_template("login.html")


#Logowanko urzytkownika czy cos takiego 

@app.route("/user", methods=['POST','GET'])
def user():
    email = None

    if "user" in session:
        user = session["user"]

        if request.method == 'POST':
            email= request.form["email"]
            session["email"]=email
            flash("Email seved")

        return render_template("user.html", email=email)
    else:
        flash("You are not loge in ")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user",None)
    flash("you have been logged out!")
    session.pop("use",None)
    session.pop("email",None)
    return redirect(url_for("login"))



if __name__=="__main__":
    db.create_all()
    app.run(debug=True)