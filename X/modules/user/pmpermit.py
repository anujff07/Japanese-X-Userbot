from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.exc import IntegrityError

from config import CMD_HANDLER
from X import TEMP_SETTINGS
from X.helpers.adminHelpers import DEVS
from X.helpers.basic import edit_or_reply
from X.helpers.SQL.globals import addgvar, delgvar, gvarstatus
from X.helpers.SQL.pm_permit_sql import approve, dissprove, is_approved
from X.helpers.tools import get_arg
from .help import *

DEF_UNAPPROVED_MSG = """Hᴇʟʟᴏ sɪʀ ᴍʏsᴇʟғ Jᴀᴘᴀɴᴇsᴇ-X-Usᴇʀʙᴏᴛ, ғᴏʀ {mention} Pʀᴏᴛᴇᴄᴛɪᴏɴ 
Hᴇʏ ᴛʜᴇʀᴇ!! I'ᴍ Jᴀᴘᴀɴᴇsᴇ-X-Usᴇʀʙᴏᴛ ᴀɴᴅ I'ᴍ ʜᴇʀᴇ ᴛᴏ Pʀᴏᴛᴇᴄᴛ {mention} ..
Dᴏɴ'ᴛ Uɴᴅᴇʀ Esᴛɪᴍᴀᴛᴇ ᴍᴇ 😈😈
Mʏ Mᴀsᴛᴇʀ {mention} ɪs ʙᴜsʏ ʀɪɢʜᴛ ɴᴏᴡ !! 
"
Mʏ Mᴀsᴛᴇʀ ʜᴀs ᴀssɪɢɴᴇᴅ ᴍᴇ ᴛʜᴇ ᴅᴜᴛʏ ᴛᴏ ᴋᴇᴇᴘ ᴀ ᴄʜᴇᴄᴋ ᴏɴ ʜɪs PM, Aɴᴅ ɪ'ʟʟ ᴅᴏ ɪᴛ ғᴀɪᴛʜғᴜʟʟʏ..Sᴏ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴅɪsᴛᴜʀʙ ʜɪᴍ..
Iғ ᴜ Sᴘᴀᴍ, ᴏʀ ᴛʀɪᴇᴅ ᴀɴʏᴛʜɪɴɢ ғᴜɴɴʏ, I'ᴠᴇ ғᴜʟʟ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ Bʟᴏᴄᴋ + Rᴇᴘᴏʀᴛ ʏᴏᴜ ᴀs Sᴘᴀᴍ ɪɴ Tᴇʟᴇɢʀᴀᴍ's sᴇʀᴠᴇʀ...
Bᴇᴛᴛᴇʀ ʙᴇ ᴄᴀʀᴇғᴜʟ..
Cʜᴏᴏsᴇ ᴀɴʏ Rᴇᴀsᴏɴ & GTFO**"""


@Client.on_message(filters.private & ~filters.me & ~filters.bot & filters.incoming, group=69)
async def incomingpm(client: Client, message: Message):
    try:
        from X.helpers.SQL.globals import gvarstatus, addgvar, delgvar
        from X.helpers.SQL.pm_permit_sql import is_approved, approve, dissprove
    except BaseException:
        pass

    if gvarstatus("PMPERMIT") == "false":
        return
    if await auto_accept(client, message) or message.from_user.is_self:
        message.continue_propagation()
    if message.chat.id != 777000:
        PM_LIMIT = int(gvarstatus("PM_LIMIT") or 5)
        getmsg = gvarstatus("unapproved_msg")
        UNAPPROVED_MSG = getmsg if getmsg is not None else DEF_UNAPPROVED_MSG.format(mention=message.from_user.mention)

        apprv = is_approved(message.chat.id)
        if not apprv and message.text != UNAPPROVED_MSG:
            if message.chat.id in TEMP_SETTINGS["PM_LAST_MSG"]:
                prevmsg = TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                if message.text != prevmsg:
                    async for msg in client.search_messages(message.chat.id, from_user="me", limit=10, query=UNAPPROVED_MSG):
                        await msg.delete()
                    if TEMP_SETTINGS["PM_COUNT"].get(message.chat.id, 0) < (PM_LIMIT - 1):
                        ret = await message.reply_text(
                            UNAPPROVED_MSG,
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("Owner", user_id="6694740726"), InlineKeyboardButton("Support", url="https://t.me/Japanese_Userbot_Chat")],
                                [InlineKeyboardButton("Channel", url="https://t.me/Japanese_Userbot")]
                            ])
                        )
                        TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            else:
                ret = await message.reply_text(
                    UNAPPROVED_MSG,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Owner", user_id="6694740726"), InlineKeyboardButton("Support", url="https://t.me/Japanese_Userbot_Chat")],
                        [InlineKeyboardButton("Channel", url="https://t.me/Japanese_Userbot")]
                    ])
                )
                TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text

            TEMP_SETTINGS["PM_COUNT"][message.chat.id] = TEMP_SETTINGS["PM_COUNT"].get(message.chat.id, 0) + 1
            if TEMP_SETTINGS["PM_COUNT"][message.chat.id] > (PM_LIMIT - 1):
                await message.reply("**Sorry, you have been blocked due to spam chat**")
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass
                await client.block_user(message.chat.id)

    message.continue_propagation()


async def auto_accept(client, message):
    if message.chat.id in DEVS:
        try:
            approve(message.chat.id)
            await client.send_message(
                message.chat.id,
                f"<b>Receiving Messages!!!</b>\n{message.from_user.mention} <b>Developer Detected Japanese-X-Userbot🔥</b>",
                parse_mode="html"
            )
        except IntegrityError:
            pass

    if message.chat.id not in [client.me.id, 777000]:
        if is_approved(message.chat.id):
            return True

        async for msg in client.iter_history(message.chat.id, limit=1):
            if msg.from_user.id == client.me.id:
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                try:
                    approve(message.chat.id)
                    async for msg in client.search_messages(message.chat.id, from_user="me", limit=10, query=UNAPPROVED_MSG):
                        await msg.delete()
                    return True
                except BaseException:
                    pass

    return False


@Client.on_message(filters.command(["ok", "setuju", "approve"], CMD_HANDLER) & filters.me & filters.private)
async def approvepm(client: Client, message: Message):
    try:
        approve(message.reply_to_message.from_user.id)
        await message.edit(f"**Receiving Messages From** {message.reply_to_message.from_user.mention}!")
    except BaseException as e:
        await message.edit(str(e))


@Client.on_message(filters.command(["tolak", "nopm", "disapprove"], CMD_HANDLER) & filters.me & filters.private)
async def disapprovepm(client: Client, message: Message):
    try:
        dissprove(message.reply_to_message.from_user.id)
        await message.edit(f"**Message** {message.reply_to_message.from_user.mention} **Has been Rejected, Please Do Not Do It Spam Chat!**")
    except BaseException as e:
        await message.edit(str(e))


@Client.on_message(filters.command("pmlimit", CMD_HANDLER) & filters.me)
async def setpm_limit(client: Client, message: Message):
    if gvarstatus("PMPERMIT") == "false":
        return await message.edit(f"**You Have To Set Var** `PM_AUTO_BAN` **When** `True`\n\n**If you want to activate PMPERMIT Please Type:** `{CMD_HANDLER}setvar PM_AUTO_BAN True`")
    try:
        input_str = message.text.split(None, 1)[1]
        PM_LIMIT = int(input_str)
        addgvar("PM_LIMIT", PM_LIMIT)
        await message.edit(f"**Set PM limit to** `{PM_LIMIT}`")
    except BaseException as e:
        await message.edit(str(e))


@Client.on_message(filters.command(["pmpermit", "pmguard"], CMD_HANDLER) & filters.me)
async def onoff_pmpermit(client: Client, message: Message):
    h_type = True if message.command[1].lower() == "on" else False
    PMPERMIT = True if gvarstatus("PMPERMIT") != "false" else False
    if PMPERMIT:
        if h_type:
            await edit_or_reply(message, "**PMPERMIT Already Activated**")
        else:
            addgvar("PMPERMIT", h_type)
            await edit_or_reply(message, "**PMPERMIT Shutdown Successfully**")
    elif h_type:
        addgvar("PMPERMIT", h_type)
        await edit_or_reply(message, "**PMPERMIT Activated Successfully**")
    else:
        await edit_or_reply(message, "**PMPERMIT It's Turned Off**")


@Client.on_message(filters.command("setpmpermit", CMD_HANDLER) & filters.me)
async def stpmpt(client: Client, message: Message):
    if gvarstatus("PMPERMIT") == "false":
        return await message.edit(f"**You Have To Tune In Var** `PM_AUTO_BAN` **When** `True`\n\n**If you want to activate PMPERMIT Please Type:** `{CMD_HANDLER}setvar PM_AUTO_BAN True`")
    try:
        input_msg = message.reply_to_message
        if input_msg:
            msg = input_msg.text
            addgvar("unapproved_msg", msg)
            await message.edit("**Message Successfully Saved to Chat Room**")
        else:
            await message.edit("**Please reply to the message**")
    except BaseException as e:
        await message.edit(str(e))


@Client.on_message(filters.command("getpmpermit", CMD_HANDLER) & filters.me)
async def gtpmprmt(client: Client, message: Message):
    if gvarstatus("PMPERMIT") == "false":
        return await message.edit(f"**You Have To Tune In Var** `PM_AUTO_BAN` **When** `True`\n\n**If you want to activate PMPERMIT Please Type:** `{CMD_HANDLER}setvar PM_AUTO_BAN True`")
    try:
        custom_message = gvarstatus("unapproved_msg")
        if custom_message is not None:
            await message.edit("**Order PMPERMIT Now:**" f"\n\n{custom_message}")
        else:
            await message.edit("**You Have Not Set PMPERMIT Custom Message,**\n" f"**Still Using Default PM Message:**\n\n{DEF_UNAPPROVED_MSG}")
    except BaseException as e:
        await message.edit(str(e))


@Client.on_message(filters.command("rtpprt", CMD_HANDLER) & filters.me)
async def gtpmprmt(client: Client, message: Message):
    if gvarstatus("PMPERMIT") == "false":
        return await message.edit(f"**You Have To Tune In Var** `PM_AUTO_BAN` **When** `True`\n\n**If you want to activate PMPERMIT, please type:** `{CMD_HANDLER}setvar PM_AUTO_BAN True`")
    try:
        custom_message = gvarstatus("unapproved_msg")
        if custom_message is None:
            await message.edit("**Your PMPERMIT message is already default**")
        else:
            delgvar("unapproved_msg")
            await message.edit("**Successfully Changed PMPERMIT Custom Message to Default**")
    except BaseException as e:
        await message.edit(str(e))


add_command_help(
    "pmpermit",
    [
        [
            f"ok or {CMD_HANDLER}setuju",
            "Receive someone's message by replying to their message or tags and also to do in pm",
        ],
        [
            f"minus or {CMD_HANDLER}nopm",
            "Reject someone's message by replying to the message or tags and also to do in pm",
        ],
        [
            "pmlimit <number>",
            "To customize the auto block message limit message",
        ],
        [
            "pmpermit on/off",
            "To enable or disable PMPERMIT",
        ],
    ],
)
