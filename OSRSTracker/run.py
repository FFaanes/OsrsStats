from flask import Flask
from flask import request, session, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

import os

import stat_processor as OsrsStats
from config import setup_app


# Setup Flask Server and sqlalchemy db
app, db = setup_app()

# Database Classes
class OSRSPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

@app.route("/", methods=["GET","POST"])
def main():        
    if request.method == "POST":
        username = request.form.get("form_username")
        player = OsrsStats.OsrsPlayer(username)

        if player.player_exists == True:
            session["username"] = username
            session["player_exists"] = player.player_exists
            session["skills"] = player.skills(raw=True, display=False)
            return redirect(url_for(".player_page", username=session["username"]))
        else:
            return render_template("home_page/home.html")
    else:
        return render_template("home_page/home.html")
    

@app.route("/<username>", methods=["GET","POST"])
def player_page(username):
    if username in session["username"]:
        username = session["username"]
        player_exists = session["player_exists"]
        skills = session["skills"]
    else:
        player = OsrsStats.OsrsPlayer(username)
        if player.player_exists == True:
            session["username"] = player.username
            session["player_exists"] = player.player_exists
            session["skills"] = player.skills(raw=True, display=False)
            return render_template(f"player_page/player.html", username=session["username"], player_exists=session["player_exists"], skills=session["skills"])

        return redirect(url_for(".main"))
        
    if request.method == "GET":
        return render_template(f"player_page/player.html", username=username, player_exists=player_exists, skills=skills)
    
    if request.method == "POST":
        player = OsrsStats.OsrsPlayer(session["username"])
        for skill in player._skill_stats:
            player._skill_stats[skill] = session["skills"][skill]

        changes = player.compare()[0]
        skills = session["skills"]

        print(changes)
        return render_template(f"player_page/player.html", username=username, player_exists=player_exists, skills=skills, changes=changes)


# Start Server
if __name__ == "__main__":
    app.run()