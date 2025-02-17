from flask import flash, redirect, url_for, render_template, session
from app import app, mongodb
from werkzeug.security import check_password_hash

from WTForms.login import LoginForm


@app.route("/")
def home():
    return render_template("layout.html", loginForm=LoginForm())


@app.route("/login", methods=["POST", "GET"])
def userLogin():
    userLoginForm = LoginForm()
    if userLoginForm.validate_on_submit():
        emailID = userLoginForm.emailID.data
        password = userLoginForm.password.data

        userLoginForm.emailID.data = ""
        userLoginForm.password.data = ""

        user = mongodb.users.find_one({"EmailID": emailID})
        if user and check_password_hash(user["Password"], password):
            session.permanent = True
            session["emailID"] = emailID
            return redirect(url_for("promptIndex"))
        else:
            flash(
                f"Your EmailID - {emailID} not found in Database or Recheck your Password."
            )
    return redirect(url_for("home"))
