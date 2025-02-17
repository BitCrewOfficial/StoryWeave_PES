from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from app import app, mongodb

from WTForms.signup import SignupForm


@app.route("/signup", methods=["POST", "GET"])
def UserSignupForm():
    return render_template("userSignup.html", userSignupForm=SignupForm())


@app.route("/signin", methods=["POST", "GET"])
def Signin():
    userSignupForm = SignupForm()
    if userSignupForm.validate_on_submit():
        name = userSignupForm.name.data
        emailID = userSignupForm.emailID.data
        password = generate_password_hash(userSignupForm.password.data)

        userSignupForm.name.data = ""
        userSignupForm.emailID.data = ""
        userSignupForm.password.data = ""

        if mongodb.Admins.find_one({"EmailID": emailID}):
            flash("EmailID Already Exists. Try to Login with your Password.")
            return redirect(url_for("UserIndex"))
        else:
            mongodb.users.insert_one(
                {"Name": name, "EmailID": emailID, "Password": password}
            )
            flash(f"User Added Successfully. Your EmailID - {emailID}.")
    return redirect(url_for("home"))
