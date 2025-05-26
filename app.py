from flask import Flask, redirect, url_for, render_template, session, request
from flask_session import Session
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Session(app)
discord = DiscordOAuth2Session(app)

@app.route("/")
def index():
    if not discord.authorized:
        return redirect(url_for("login"))
    user = discord.fetch_user()
    guilds = discord.fetch_guilds()
    return render_template("home.html", user=user, guilds=guilds)

@app.route("/login/")
def login():
    return discord.create_session()

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for("index"))

@app.route("/logout/")
def logout():
    discord.revoke()
    session.clear()
    return redirect(url_for("index"))

@app.route("/ticket/", methods=["GET", "POST"])
@requires_authorization
def ticket():
    if request.method == "POST":
        issue = request.form.get("issue")
        # Handle ticket submission logic here
        return render_template("ticket.html", success=True)
    return render_template("ticket.html", success=False)

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
