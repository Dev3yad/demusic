
import os
from os import path
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from Client import callsmusic, queues
from Client.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import yt_dlp
from youtube_search import YoutubeSearch
import converter
from youtube import youtube
from config import DURATION_LIMIT, que, SUDO_USERS, BOT_USERNAME, UPDATES_CHANNEL, GROUP_SUPPORT, ASSISTANT_USERNAME
from cache.admins import admins as a
from helpers.filters import command
from helpers.decorators import errors, authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from helpers.channelmusic import get_chat_id
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream

# plus
chat_id = None
useer = "NaN"


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes or cb.from_user.id in SUDO_USERS:
            return await func(client, cb)
        await cb.answer("ليس مسموح لك بالصغط", show_alert=True)
        return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")

@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
@cb_admin_check
@authorized_users_only
async def m_cb(b, cb):
    global que
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat

    if type_ == "cls":
        await cb.answer("تم اغلاء القائمة", show_alert=True)
        await cb.message.delete()


# play
@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & filters.group & ~filters.edited & ~filters.forwarded & ~filters.via_bot)
async def play(_, message: Message):
    global que
    global useer
    lel = await message.reply("🔄 **معالجة...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "الحساب المساعد"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                await lel.edit(
                    "<b>تذكر ان تضيف الحساب المساعد</b>",
                )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>اعطني صلاحية دعوة المستخدمين لدعوة الحساب المساعد\nاو قم بي اضافتة يدويا @{ASSISTANT_USERNAME}</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "انضممت هنا لتشغيل الموسيقي",
                    )
                    await lel.edit(
                        "<b>انضم الحساب المساعد الي مجموعك جاري تشغيل الموسيقي</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"حدث خطأ ما\n{Exception}\n\nيرجي اعادة توجية هذة الرسالة الي المطور @YYYBD\n\nقم بي اضافه الحساب المساعد يدويا @{ASSISTANT_USERNAME}")
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<b>هناك مشكلة لم استطيع دعوة الحساب المساعد ارسل الامر ( انضم ) حتا ينضم او قم بي اضافتة يدويا @{ASSISTANT_USERNAME}</b>"
        )
        return

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ مدة المقطع اطول من {DURATION_LIMIT} دقيقة لا يمكنني تشغيلها"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/cd0b87484429704c7b935.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "@YYYBD"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("مجموعة الدعم", url=f"t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton("قناة التحديثات", url=f"t.me/{UPDATES_CHANNEL}"),
                ],
                [InlineKeyboardButton(text="اغلاق القائمة", callback_data="cls")],
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("مجموعة الدعم", url=f"t.me/{GROUP_SUPPORT}"),
                        InlineKeyboardButton("قناة التحديثات", url=f"t.me/{UPDATES_CHANNEL}"),
                    ],
                    [InlineKeyboardButton(text="اغلاق القائمة", callback_data="cls")],
                ]
            )

        except Exception as e:
            title = "@YYYBD"
            thumb_name = "https://telegra.ph/file/cd0b87484429704c7b935.png"
            duration = "@YYYBD"
            views = "@YYYBD"

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ مدة الفيديو اطول من {DURATION_LIMIT} دقيقة غير مسموح لي بالتشغيل"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "لم اجد الموسيقي جرب كتابة الاسم بطريقة اخري"
            )
        await lel.edit("🔎 **البحث عن الموسيقي...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🎵 **معالجة الموسيقي...**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit("🎵 **معالجة الموسيقي...**")
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("مجموعة الدعم", url=f"t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton("قناة التحديثات", url=f"t.me/{UPDATES_CHANNEL}"),
                ],
                [InlineKeyboardButton(text="اغلاق القائمة", callback_data="cls")],
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ مدة المقطع اطول من {DURATION_LIMIT} دقيقة غير مسموح لي بالتشغيل"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="**🎵 الموسيقي :** {}\n**🕒 المدة :** {} دقيقة\n**👤 مطلوبة من قبل :** {}\n\n**#⃣ الدور :** {}".format(
                title,
                duration,
                message.from_user.mention(),
                position,
            ),
            reply_markup=keyboard,
        )
    else:
        await callsmusic.pytgcalls.join_group_call(
                message.chat.id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            ) 
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**🎵 الموسيقي :** {}\n**🕒 المدة :** {} دقيقة\n**👤 مطلوبة من قبل :** {}\n\n**▶️ يشتغل الان : `{}`...**".format(
                title, duration, message.from_user.mention(), message.chat.title
            ),
        )

    os.remove("final.png")
    return await lel.delete()
