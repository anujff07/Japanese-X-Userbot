import asyncio
import os
import time
from urllib.request import urlretrieve

import requests as r
import wget
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

from config import CMD_HANDLER
from X.helpers.basic import edit_or_reply

from .help import *


def get_text(message: Message) -> [None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@Client.on_message(filters.command(["vid", "video"], cmd) & filters.me)
async def yt_vid(client: Client, message: Message):
    input_st = message.text
    input_str = input_st.split(" ", 1)[1]
    Man = await edit_or_reply(message, "`Processing...`")
    if not input_str:
        await Man.edit_text(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    await Man.edit_text(f"`Searching {input_str} From Youtube. Please Wait.`")
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    result_s = rt["search_result"]
    url = result_s[0]["link"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await Man.edit_text(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    time.time()
    file_path = f"{ytdl_data['id']}.mp4"
    capy = f"**Video Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    await client.send_video(
        message.chat.id,
        video=open(file_path, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=downloaded_thumb,
        caption=capy,
        supports_streaming=True,
    )
    await Man.delete()
    for files in (downloaded_thumb, file_path):
        if files and os.path.exists(files):
            os.remove(files)


@Client.on_message(filters.command("song", cmd) & filters.me)
async def song(client: Client, message: Message):
    input_str = get_text(message)
    rep = await edit_or_reply(message, "`Processing...`")
    if not input_str:
        await rep.edit(
            "`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`"
        )
        return
    await rep.edit(f"`Getting {input_str} From Youtube Servers. Please Wait.`")
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    result_s = rt["search_result"]
    url = result_s[0]["link"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await rep.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    time.time()
    file_path = f"{ytdl_data['id']}.mp3"
    capy = f"**Song Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    await client.send_audio(
        message.chat.id,
        audio=open(file_path, "rb"),
        title=str(ytdl_data["title"]),
        performer=str(ytdl_data["uploader"]),
        thumb=downloaded_thumb,
        caption=capy,
    )
    await rep.delete()
    for files in (downloaded_thumb, file_path):
        if files and os.path.exists(files):
            os.remove(files)


@Client.on_message(filters.command(["saavn"]) & filters.me)
async def saavn_dl(client: Client, message: Message):
    song = get_text(message)
    if not song:
        return await message.edit_text("`Give me something to search`")

    lol = await edit_or_reply(message, "`Searching on Saavn...`")
    sung = song.replace(" ", "%20")
    url = f"https://jostapi.herokuapp.com/saavn?query={sung}"
    
    try:
        response = r.get(url)
        data = response.json()
        if not data:
            return await lol.edit("`Song not found..`")
        
        song_data = data[0]
        title = song_data.get("song")
        media_url = song_data.get("media_url")
        img = song_data.get("image")
        singers = song_data.get("singers")
        
        if not (title and media_url and img and singers):
            return await lol.edit("`Song information not found..`")
        
        file_name = f"{title}.mp3"
        image_name = f"{title}.jpg"
        
        urlretrieve(media_url, file_name)
        urlretrieve(img, image_name)
        await lol.delete()
        
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_name,
            caption=f"Song from Saavan uploaded by Japanese XUserbot\nSong name: {title}\nSingers: {singers}",
        )
        
        os.remove(file_name)
        os.remove(image_name)
        
    except Exception as e:
        await lol.edit(f"Error: {str(e)}")


@Client.on_message(filters.command(["deezer"]) & filters.me)
async def deezergeter(client: Client, message: Message):
    rep = await edit_or_reply(message, "`Searching for song on Deezer...`")
    sgname = get_text(message)
    if not sgname:
        await rep.edit("`Please provide a valid input. You can check the help menu to know more!`")
        return
    
    link = f"https://api.deezer.com/search?q={sgname}&limit=1"
    response = r.get(url=link)
    data = response.json().get("data", [])
    
    if not data:
        await rep.edit("`Song not found. Try searching for some other song`")
        return
    
    urlhp = data[0]
    urlp = urlhp.get("link")
    thumbs = urlhp["album"]["cover_big"]
    thum_f = wget.download(thumbs)
    polu = urlhp.get("artist")
    replo = urlp[29:]
    urlp = f"https://starkapis.herokuapp.com/deezer/{replo}"
    datto = r.get(url=urlp).json()
    mus = datto.get("url")
    sname = f"{urlhp.get('title')}.mp3"
    doc = r.get(mus)
    
    await client.send_chat_action(message.chat.id, "upload_audio")
    await rep.edit("`Downloading song from Deezer...`")
    
    with open(sname, "wb") as f:
        f.write(doc.content)
        
    car = f"""
**Song Name:** {urlhp.get("title")}
**Duration:** {urlhp.get('duration')} Seconds
**Artist:** {polu.get("name")}
Music downloaded and uploaded by Japanese X Userbot"""
    
    await rep.edit(f"`Downloaded {sname}! Now uploading song...`")
    
    await client.send_audio(
        chat_id=message.chat.id,
        audio=open(sname, "rb"),
        duration=int(urlhp.get("duration")),
        title=str(urlhp.get("title")),
        performer=str(polu.get("name")),
        thumb=thum_f,
        caption=car,
    )
    
    await client.send_chat_action(message.chat.id, "cancel")
    await rep.delete()


add_command_help(
    "youtubedl",
    [
        ["song", "Download Audio From YouTube."],
        [
            "video",
            "Download Video from YouTube ",
        ],
    ],
)

add_command_help(
    "song",
    [
        ["deezer", "Download From Deezer."],
        [
            "saavn",
            "Download From Saavn",
        ],
    ],
)
