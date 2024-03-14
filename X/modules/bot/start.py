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
    message = "Lol Who is a Dog!!!!"
    client.send_message(user_id, message)
    client.answer_callback_query(callback_query.id, text="Message sent")

logoX = [
    "https://graph.org/file/0ed7be5cf4fdbf052afa9.jpg"
]

alive_logo = random.choice(logoX)

@app.on_message(filters.command("start") & filters.private)
async def start(app, message):
    chat_id = message.chat.id
    file_id = alive_logo
    caption = "Hi, I am Asisstant Japanese-X-Userbot\n What bro? If you want to be angry, you really have a tattoo?."
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Support", url="https://t.me/Japanese_Userbot_Chat"),
            InlineKeyboardButton("Channel", url="https://t.me/Japanese_Useebot"),]
            [InlineKeyboardButton("Owner", user_id=6694740726),
        ],
    ])

    await app.send_photo(chat_id, file_id, caption=caption, reply_markup=reply_markup)
