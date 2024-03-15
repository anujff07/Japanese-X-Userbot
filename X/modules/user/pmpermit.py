from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup 
from pyrogram import filters

from X import app

sudo_users = []
def is_sudo(user_id):
    return user_id in sudo_users

caption=f"""Hᴇʟʟᴏ sɪʀ ᴍʏsᴇʟғ Jᴀᴘᴀɴᴇsᴇ-X-Usᴇʀʙᴏᴛ, ғᴏʀ {message.from_user.mention} Pʀᴏᴛᴇᴄᴛɪᴏɴ 
Hᴇʏ ᴛʜᴇʀᴇ!! I'ᴍ Jᴀᴘᴀɴᴇsᴇ-X-Usᴇʀʙᴏᴛ ᴀɴᴅ I'ᴍ ʜᴇʀᴇ ᴛᴏ Pʀᴏᴛᴇᴄᴛ {message.from_user.mention} ..
Dᴏɴ'ᴛ Uɴᴅᴇʀ Esᴛɪᴍᴀᴛᴇ ᴍᴇ 😈😈
Mʏ Mᴀsᴛᴇʀ {message.from_user.mention} ɪs ʙᴜsʏ ʀɪɢʜᴛ ɴᴏᴡ !! 
"
Mʏ Mᴀsᴛᴇʀ ʜᴀs ᴀssɪɢɴᴇᴅ ᴍᴇ ᴛʜᴇ ᴅᴜᴛʏ ᴛᴏ ᴋᴇᴇᴘ ᴀ ᴄʜᴇᴄᴋ ᴏɴ ʜɪs PM, Aɴᴅ ɪ'ʟʟ ᴅᴏ ɪᴛ ғᴀɪᴛʜғᴜʟʟʏ..Sᴏ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴅɪsᴛᴜʀʙ ʜɪᴍ..
Iғ ᴜ Sᴘᴀᴍ, ᴏʀ ᴛʀɪᴇᴅ ᴀɴʏᴛʜɪɴɢ ғᴜɴɴʏ, I'ᴠᴇ ғᴜʟʟ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ Bʟᴏᴄᴋ + Rᴇᴘᴏʀᴛ ʏᴏᴜ ᴀs Sᴘᴀᴍ ɪɴ Tᴇʟᴇɢʀᴀᴍ's sᴇʀᴠᴇʀ...
Bᴇᴛᴛᴇʀ ʙᴇ ᴄᴀʀᴇғᴜʟ..
Cʜᴏᴏsᴇ ᴀɴʏ Rᴇᴀsᴏɴ & GTFO**""";

x=await message.reply_text(message.from_user.mention) 
y=await message.reply_text(app.me.mention)
await app.send_message(
    message.chat.id, caption,
    reply_markup=InlineKeyboardMarkup(
        [
                     [InlineKeyboardButton("Owner", user_id="6694740726"), InlineKeyboardButton("Support", url="https://t.me/Japanese_Userbot_Chat")],
            [InlineKeyboardButton("Channel", url="https://t.me/Japanese_Userbot")]]))