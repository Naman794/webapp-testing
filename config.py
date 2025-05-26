import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "669218CABDA3BDE5")
    SESSION_TYPE = "filesystem"
    
    # Discord OAuth2 Configuration
    GUILD_ID = int(os.getenv("GUILD_ID", "720914167652941846"))
    DISCORD_CLIENT_ID = os.getenv("CLIENT_ID", "741322048726368286")
    DISCORD_CLIENT_SECRET = os.getenv("CLIENT_SECRET", "t90BwTah09VJqpTPU7e9X-yxjrGZ-KW9")
    DISCORD_REDIRECT_URI = os.getenv("REDIRECT_URI", "http://dono-01.danbot.host:1646/callback")
    
    OAUTH2_SCOPE = ["identify", "guilds.join"]
    OAUTH2_BASE_URL = "https://discord.com/oauth2/authorize"
    OAUTH2_TOKEN_URL = "https://discord.com/api/oauth2/token"
