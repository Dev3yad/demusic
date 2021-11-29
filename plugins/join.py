# Credit DaisyXMusic, Changes By Blaze, Improve Code By Decode

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from Client.callsmusic import client as USER
from config import SUDO_USERS, BOT_USERNAME, ASSISTANT_USERNAME
from helpers.filters import command

@Client.on_message(command(["ubjoin","userbotjoin","join", f"ubjoin@{BOT_USERNAME}", f"userbotjoin@{BOT_USERNAME}", f"join@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>أضفني كمسؤول في مجموعتك أولاً</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "الحساب المساعد"

    try:
        await USER.join_chat(invitelink)
        await USER.reply("انضممت هنا كما طلبت")
        await message.reply_text(
        "<b>انضم الحساب المساعد إلى محادثتك</b>",
    )
    except UserAlreadyParticipant:
        await USER.reply("انا موجود هنا")
        await message.reply_text(
            "<b>الحساب المساعد بالفعل في الدردشة الخاصة بك</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
                        f"حدث خطأ ما\n{e}\n\nيرجي اعادة توجية هذة الرسالة الي المطور @YYYBD \n\nقم بي اضافه الحساب المساعد يدويا @{ASSISTANT_USERNAME}")
        return

@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>لا امتلك صلاحية دعوة المستخدمين</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "الحساب المساعد0"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await USER.reply("انا موجود هنا")
        await message.reply_text(
            "<b>الحساب المساعد بالفعل في الدردشة الخاصة بك</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
                        f"حدث خطأ ما\n{e}\n\nيرجي اعادة توجية هذة الرسالة الي المطور @YYYBD \n\nقم بي اضافه الحساب المساعد يدويا @{ASSISTANT_USERNAME}")
        return
    await USER.reply("انضممت هنا كما طلبت")
    await message.reply_text(
        "<b>انضم الحساب المساعد إلى محادثتك</b>",
    )


@USER.on_message(command(["ubleave","userbotleave","leave", f"ubleave@{BOT_USERNAME}", f"userbotleave@{BOT_USERNAME}", f"leave@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot)
@authorized_users_only
async def rem(USER, message):
    try:
        await message.reply_text("سوف اغادر")
        await USER.leave_chat(message.chat.id)
    except Exception as e:
        await message.reply_text("حدث خطأ ما\n{e}\n\nيرجي اعادة توجية هذة الرسالة الي المطور @YYYBD \n\nقم بي طرد الحساب المساعد يدويا @{ASSISTANT_NAME}")
        return


@Client.on_message(command(["ubleaveall","userbotleaveall","leaveall", f"ubleaveall@{BOT_USERNAME}", f"userbotleaveall@{BOT_USERNAME}", f"leaveall@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot)
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("الحساب المساعد سوف يغادر جميع الدردشات")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left=left+1
                await lol.edit(f"الحساب المساعد ترك... {left} محادثة. فشل: {failed} محادثة.")
            except:
                failed=failed+1
                await lol.edit(f"الحساب المساعد ترك... {left} محادثة. فشل: {failed} محادثة.")
        await client.send_message(message.chat.id, f"الحساب المساعد خرج من {left} محادثة. فشل {failed} محادثة.")
