from flask import Flask, redirect, url_for, render_template, session, request
from flask_session import Session
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from config import Config
import requests
import os

app = Flask(__name__)
app.config.from_object(Config)

# Session and OAuth Setup
Session(app)
discord = DiscordOAuth2Session(app)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Required for adding user to guild

@app.route("/")
def index():
    if not discord.authorized:
        return redirect(url_for("login"))
    
    user = discord.fetch_user()
    guilds = discord.fetch_guilds()

    return render_template("home.html", user=user, guilds=guilds)

@app.route("/login/")
def login():
    return discord.create_session(scope=Config.OAUTH2_SCOPE)

@app.route("/callback/")
def callback():
    discord.callback()

    # Join user to guild
    user = discord.fetch_user()
    access_token = discord.token["access_token"]
    guild_id = Config.GUILD_ID

    url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{user.id}"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    json_data = {
        "access_token": access_token
    }

    response = requests.put(url, headers=headers, json=json_data)
    if response.status_code not in (201, 204):
        print(f"[ERROR] Failed to add user to guild: {response.status_code}, {response.text}")

    return redirect(url_for("index"))

@app.route("/logout/")
def logout():
    discord.revoke()
    session.clear()
    return redirect(url_for("index"))

@app.route("/ticket/", methods=["GET", "POST"])
@requires_authorization
def ticket():
    user = discord.fetch_user()
    if request.method == "POST":
        issue = request.form.get("issue")
        print(f"[TICKET] From {user.name}#{user.discriminator}: {issue}")
        return render_template("ticket.html", success=True, user=user)
    return render_template("ticket.html", success=False, user=user)

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 1646))
