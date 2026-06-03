import json
import os


def get_user_list(config, key):
    with open("{}/Razerbot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


def get_env_list(key, default=[]):
    val = os.environ.get(key)
    if not val:
        return default
    try:
        return [int(x.strip()) for x in val.split(",") if x.strip().isdigit()]
    except Exception:
        return default


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    API_ID = int(os.environ.get("API_ID", 123456))  # integer value, dont use ""
    API_HASH = os.environ.get("API_HASH", "API_HASH")
    TOKEN = os.environ.get("TOKEN", "BOT_TOKEN")  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "BOT_USERNAME")
    BOT_NAME = os.environ.get("BOT_NAME", "file alter")
    BOT_ID = os.environ.get("BOT_ID", "")
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "YourUsername")
    START_IMG = os.environ.get("START_IMG", "https://graph.org/file/644fddccf30ac191fc895.jpg")
    ALIVE_IMG = os.environ.get("ALIVE_IMG", "https://graph.org/file/36c17c0f22aeea9c99895.jpg")
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "<channel-username>") # Your own channel for updates, do not add the @
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "<support-chat-username>")  # Your own group for support, do not add the @
    JOIN_LOGGER = int(os.environ.get("JOIN_LOGGER", -10012345678))  # A new channel ID To log who started the bot. Starting with "-100", Put inside braces
    EVENT_LOGS = int(os.environ.get("EVENT_LOGS", -10012345678))  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit

    # RECOMMENDED
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "") 
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db"))  # needed for any database module
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = os.environ.get("WEBHOOK", "False").lower() in ("true", "1", "yes")
    INFOPIC = os.environ.get("INFOPIC", "True").lower() in ("true", "1", "yes")
    URL = os.environ.get("URL", None)
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", "")  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", "@SpamWatchSupport")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    
    # OPTIONAL
    DRAGONS = get_env_list("DRAGONS", [])  ##List of integer ids separated by "," for users which have sudo access to the bot.
    DEV_USERS = get_env_list("DEV_USERS", []) ##List of integer ids separated by ","  for developers who will have the same perms as the owner
    DEMONS = get_env_list("DEMONS", []) ##List of integer ids separated by ","  for users which are allowed to gban, but can also be banned.
    TIGERS = get_env_list("TIGERS", []) ##List of integer ids separated by ","  for users which WONT be banned/kicked by the bot.
    WOLVES = get_env_list("WOLVES", [])
    CERT_PATH = os.environ.get("CERT_PATH", None)
    PORT = int(os.environ.get("PORT", 5000))
    DEL_CMDS = os.environ.get("DEL_CMDS", "True").lower() in ("true", "1", "yes")  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = os.environ.get("STRICT_GBAN", "True").lower() in ("true", "1", "yes")
    WORKERS = int(os.environ.get("WORKERS", 8))  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = os.environ.get("BAN_STICKER", "")  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", "True").lower() in ("true", "1", "yes")  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", "")  # Get your API key from https://www.alphavantage.co/support/#api-key
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", "")
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", "")
    TIME_API_KEY = os.environ.get("TIME_API_KEY", "")  # Get your API key from https://timezonedb.com/api
    AI_API_KEY = os.environ.get("AI_API_KEY", "")  # For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = get_env_list("BL_CHATS", [])  # List of groups that you want blacklisted.
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", "True").lower() in ("true", "1", "yes")
    SPAMMERS = os.environ.get("SPAMMERS", None)

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
