from plugins import check_heroku
from helpers.filters import command
from pyrogram import Client, filters
from helpers.decorators import sudo_users_only
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from config import BOT_USERNAME

@Client.on_message(command(["restart", "reboot", f"restart@{BOT_USERNAME}", f"reboot@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
@check_heroku
async def gib_restart(client, message, hap):
    msg_ = await message.reply_text("**🔄 جاري اعادة التشغيل...**")
    hap.restart()
