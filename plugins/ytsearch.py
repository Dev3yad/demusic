import logging

from pyrogram.types import Message
from search_engine_parser import GoogleSearch
from youtube_search import YoutubeSearch

from pyrogram import Client
from helpers.filters import command

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(command(["search"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("اكتب بحث + البحث")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("جاري البحث....")
        results = YoutubeSearch(query, max_results=5).to_dict()
        text = ""
        for i in range(5):
            text += f"العنوان - {results[i]['title']}\n"
            text += f"المدة - {results[i]['duration']}\n"
            text += f"المشاهدات - {results[i]['views']}\n"
            text += f"القناة - {results[i]['channel']}\n"
            text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
