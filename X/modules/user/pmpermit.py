# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de


from pyrogram import Client, enums, filters
from pyrogram.types import Message
from sqlalchemy.exc import IntegrityError

from config import CMD_HANDLER
from X import TEMP_SETTINGS
from X.helpers.adminHelpers import DEVS
from X.helpers.basic import edit_or_reply
from X.helpers.SQL.globals import addgvar, gvarstatus
from X.helpers.tools import get_arg

from .help import *

DEF_UNAPPROVED_MSG = (
 "❏ ᴘᴍ sᴇᴄᴜʀɪᴛʏ ᴏғ  ˹Jᴀᴘᴀɴᴇsᴇ-X-Usᴇʀʙᴏᴛ˼ !\n"
"├ Mᴏsᴛ Pᴏᴡᴇʀғᴜʟ ᴀɴᴅ Aᴅᴠᴀɴᴄᴇ Tᴇʟᴇɢʀᴀᴍ Usᴇʀʙᴏᴛ\n"
"├ Mʏ Mᴀsᴛᴇʀ ɪs Bᴜsʏ ʀɪɢʜᴛ ɴᴀᴍᴇ sᴏ Dᴏɴ'ᴛ sᴘᴀᴍ ᴘʟᴇᴀsᴇ ᴏᴛʜᴇʀᴡɪsᴇ I ᴡɪʟʟ ʙʟᴏᴄᴋ ʏᴏᴜ\n"
"╰ Pᴏᴡᴇʀᴇᴅ ʙʏ Jᴀᴘᴀɴᴇsᴇ-X-Usᴇʀʙᴏᴛ\n"
)


@Client.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69
)
async def incomingpm(client: Client, message: Message):
    try:
