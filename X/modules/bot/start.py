import random
from X import app
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from config import OWNER_ID as owner 

@app.on_callback_query()
def pmowner(client, callback_query):
    user_id = owner
    message = "𝐋𝐨𝐥 𝐖𝐡𝐨 𝐢𝐬 𝐚 𝐃𝐨𝐠!!!!"
    client.send_message(user_id, message)
    client.answer_callback_query(callback_query.id, text="Message sent")

logoX = [
    "https://graph.org/file/83978974fe5be2da118d7.jpg"
]

alive_logo = random.choice(logoX)

@app.on_message(filters.command("start") & filters.private)
async def start(app, message):
    chat_id = message.chat.id
    file_id = alive_logo
    caption = "𝐇𝐢, 𝐈 𝐚𝐦 𝐀𝐬𝐢𝐬𝐬𝐭𝐚𝐧𝐭 𝐉𝐚𝐩𝐚𝐧𝐞𝐬𝐞-𝐗-𝐔𝐬𝐞𝐫𝐛𝐨𝐭\n 𝐖𝐡𝐚𝐭 𝐛𝐫𝐨? 𝐈𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐛𝐞 𝐚𝐧𝐠𝐫𝐲, 𝐲𝐨𝐮 𝐫𝐞𝐚𝐥𝐥𝐲 𝐡𝐚𝐯𝐞 𝐚 𝐭𝐚𝐭𝐭𝐨𝐨?."
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/Japanese_Userbot_Chat"),
            InlineKeyboardButton("𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/Japanese_Useebot"),
            InlineKeyboardButton("Owner", url="https://t.me/Nobitaa_xd"),
        ],
    ])

    await app.send_photo(chat_id, file_id, caption=caption, reply_markup=reply_markup)
