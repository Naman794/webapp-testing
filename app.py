from flask import Flask, redirect, url_for, session, render_template
from flask_session import Session
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from config import (
    DISCORD_CLIENT_ID,
    DISCORD_CLIENT_SECRET,
    SECRET_KEY,
    OAUTH2_SCOPE,
    OAUTH2_BASE_URL,
    OAUTH2_TOKEN_URL
)
import os

app = Flask(__name__)

# Required Config
app.secret_key = SECRET_KEY
app.config["SESSION_TYPE"] = "filesystem"

# Discord OAuth2 Config
app.config["DISCORD_CLIENT_ID"] = DISCORD_CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = DISCORD_CLIENT_SECRET
app.config["DISCORD_REDIRECT_URI"] = os.environ["DISCORD_REDIRECT_URI"]

# OAuth2 Session
Session(app)
discord = DiscordOAuth2Session(app)

@app.route("/")
def home():
    if not discord.authorized:
        return redirect(url_for("login"))
    user = discord.fetch_user()
    return render_template("home.html", user=user)

@app.route("/login/")
def login():
    return discord.create_session(scope=OAUTH2_SCOPE)

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for("home"))

@app.route("/logout/")
def logout():
    discord.revoke()
    session.clear()
    return redirect(url_for("home"))

@app.errorhandler(Unauthorized)
def handle_unauth(e):
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
