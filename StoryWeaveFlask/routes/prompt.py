from flask import flash, redirect, url_for, render_template, session
from app import app, mongodb

from WTForms.prompt import PromptForm, HistoryButton, BackButton


@app.route("/prompt", methods=["POST", "GET"])
def promptIndex():
    if "emailID" in session:
        return render_template(
            "promptForm.html", promptForm=PromptForm(), historyButton=HistoryButton()
        )
    return redirect(url_for("home"))


@app.route("/viewHistory", methods=["POST", "GET"])
def historyIndex():
    if "emailID" in session:
        historys = mongodb.history.find({"EmailID": session.get("emailID")})
        if historys:
            return render_template(
                "viewHistory.html", historys=historys, back=BackButton()
            )
        else:
            flash("You have not prompted in the past.")
    return redirect(url_for("home"))
