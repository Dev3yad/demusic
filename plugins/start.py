from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_NAME as bn
from helpers.filters import other_filters2, command
from time import time
from datetime import datetime
from helpers.decorators import authorized_users_only
from config import BOT_USERNAME, ASSISTANT_USERNAME, UPDATES_CHANNEL, GROUP_SUPPORT

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("اسبوع", 60 * 60 * 24 * 7),
    ("يوم", 60 ** 2 * 24),
    ("ساعة", 60 ** 2),
    ("دقيقة", 60),
    ("ثانيا", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(command(["start"]) & other_filters2)
async def start(_, message: Message):
        await message.reply_photo(
        photo=f"https://t.me/{BOT_USERNAME}", 
        caption=f"""**اهلا انا بوت اسمي {bn}
استطيع تشغيل الاصوات في المحادثة الصوتية الخاصة بمجموعتك
يمكنك اضافتي الي المجموعة و تشغيل الموسيقي و الاستمتاع
ادعم ايضا الاوامر بي اللغة العربية**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                       "مجموعة المساعدة", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "قناة لتحديثات", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],[
                    InlineKeyboardButton(
                        "اضف البوت الي مجموعتك",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ]
            ]
        )
    )
