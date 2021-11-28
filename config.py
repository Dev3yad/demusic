from os import getenv

from dotenv import load_dotenv

load_dotenv()

que = {}
SESSION_NAME = getenv("SESSION_NAME")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
ASSISTANT_USERNAME = getenv("ASSISTANT_USERNAME", "AYVCMusicuser")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "YYYBR")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "VC_SUP")
BOT_USERNAME = getenv("BOT_USERNAME", "AYVCMusicbot")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/cd0b87484429704c7b935.png")
THUMB_IMG = getenv("THUMB_IMG", "https://telegra.ph/file/cd0b87484429704c7b935.png")
BOT_IMG = getenv("BOT_IMG", "https://telegra.ph/file/cd0b87484429704c7b935.png")
AUD_IMG = getenv("AUD_IMG", "https://telegra.ph/file/cd0b87484429704c7b935.png")
QUE_IMG = getenv("QUE_IMG", "https://telegra.ph/file/cd0b87484429704c7b935.png")

admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

OWNER_ID = int(getenv("OWNER_ID", "944353237"))

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "15"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "944353237").split()))
