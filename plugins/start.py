from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery, Message
from pyrogram.errors import FloodWait
import humanize
import random
from helpo.txt import mr
from helpo.database import db
from config import START_PIC, FLOOD, ADMIN 



# ===========================================================================
# ===========================================================================
                    ### AUTO RENAME = STEP 1
# ===========================================================================

import re


# Mappings
resolutions = {
    "144p": "144p",
    "240p": "240p",
    "360p": "360p",
    "480p": "480p",
    "520p": "520p",
    "640p": "640p",
    "720p": "720p",
    "1080p": "1080p",
    "1440p": "1440p",
    "2160p": "2160p",
    "4320p": "4320p",
    "4k": "4K UHD",
}

languages = {
    "HIN": "Hindi",
    "ENG": "English",
    "TAM": "Tamil",
    "TEL": "Telugu",
    "MAY": "Malayalam",
    "PAN": "Punjabi",
    "SPA": "Spanish",
    "FRE": "French",
    "GER": "German",
    "CHN": "Chinese",
    "JPN": "Japanese",
    "KOR": "Korean",
    "RUS": "Russian",
    "ARA": "Arabic",
    "POR": "Portuguese",
    "ITA": "Italian",
    "BEN": "Bengali",
    "URD": "Urdu",
    "TUR": "Turkish",
    "THA": "Thai",
    "VIE": "Vietnamese"
}


qualities = {
    "BLURAY": "BluRay",
    "WEB-DL": "WEB-DL",
    "WEBRIP": "WEBRip",
    "HDRIP": "HDRip",
    "DVDRIP": "DVDRip",
    "HDTV": "HDTV",
    "HDTS": "HDTS",
    "CamRip": "CamRip",
    "PreDvd": "PreDvd",

}
subtitles = {
    "esubs": "ESub",
    "esub": "ESub",
    "hsubs": "HSub",
    "hsub": "HSub"
}

codecs = {
    "H.264": "AVC",
    "AVC": "AVC",
    "H.265": "HEVC",
    "HEVC": "HEVC",
    "10bit HEVC": "10Bit HEVC"
}
# Updated regex patterns
season_regex = r"S(\d{1,3})"
episode_regex = r"E(\d{1,3})"
multi_episode_regex = r"E(\d{1,3})[-_](\d{1,3})"
special_episode_regex = r"S(\d{1,3})E00"

# Function to extract season, episode, resolution, quality, and languages
def extract_details(file_name):
    # Season and Episode
    season_match = re.search(season_regex, file_name, re.IGNORECASE)
    multi_episode_match = re.search(multi_episode_regex, file_name, re.IGNORECASE)
    episode_match = re.search(episode_regex, file_name, re.IGNORECASE)
    special_match = re.search(special_episode_regex, file_name, re.IGNORECASE)

    season = f"S{int(season_match.group(1)):02}" if season_match else None
    full_season = f"Season {int(season_match.group(1)):02}" if season_match else None
    if multi_episode_match:
        episode = f"E{int(multi_episode_match.group(1)):02}-{int(multi_episode_match.group(2)):02}"
        fullepisode = f"Episode {int(multi_episode_match.group(1)):02}-{int(multi_episode_match.group(2)):02}"
    elif special_match:
        episode = "Special"
        fullepisode = "Special Episode"

    elif episode_match:
        episode = f"E{int(episode_match.group(1)):02}"
        fullepisode = f"Episode {int(episode_match.group(1)):02}"
    else:
        episode = None
        fullepisode = None

    # Resolution
    resolution = None
    for key in resolutions:
        if key.lower() in file_name.lower():
            resolution = resolutions[key]
            break
    
    # codec
    codec = None 
    for key in codecs:
        if key.lower() in file_name.lower():
            codec = codecs[key]
            if key.lower() == "h.265" or key.lower() == "hevc":
                break

    # Quality
    quality = None
    for key in qualities:
        if key.lower() in file_name.lower():
            quality = qualities[key]
            break
    
    #subtitle
    subtitle = None
    for key in subtitles:
        if key.lower() in file_name.lower():
            subtitle = subtitles[key]
            break

    # Languages
    detected_languages = []
    for key in languages:
        if key.lower() in file_name.lower():
            language_name = languages[key]
            if "fandub" in file_name.lower():
                language_name += "(fanDub)"
            elif "org" in file_name.lower():
                language_name += "(ORG)"

            detected_languages.append(language_name)

    languages_list = "-".join(detected_languages) if detected_languages else None

    return season, full_season, episode, resolution, quality, subtitle, languages_list, fullepisode, codec

def extract_title(file_name):
    # Extract the title (e.g., Maeri)
    title_match = re.search(r"([A-Za-z0-9\s]+)", file_name)
    
    if title_match:
        title = title_match.group(1).strip()
        return title
    else:
        return "Unknown Title"
    
# Renaming logic
def rename_file(file_name):
    season, full_season, episode, resolution, quality, subtitle, languages_list, fullepisode, codec = extract_details(file_name)
    n_title = extract_title(file_name)   # Placeholder for extracting title (can enhance this further)
    
    n_season = f"{season} •" if season is not None else ""
    n_episode = f"{episode} •" if episode is not None else ""
    n_fullepisode = f"[{fullepisode}]" if fullepisode is not None else ""
    n_resolution = f"{resolution}" if resolution is not None else ""
    n_quality = f"{quality}" if quality is not None else ""
    n_languages = f"[{languages_list}]" if languages_list is not None else ""
    n_fullseason = f"[{full_season}]" if full_season is not None else ""
    n_subtitle = f"{subtitle}" if subtitle is not None else ""
    n_codec = f"{codec}" if codec is not None else ""

    new_name = f"{n_season} {n_episode} {n_title} {n_fullseason} {n_fullepisode} {n_resolution} {n_codec} {n_quality} {n_languages} {n_subtitle}"
    return new_name


    # new_name_parts = []
    # if season:
    #     new_name_parts.append(season)
    # if episode:
    #     new_name_parts.append(episode)
    # new_name_parts.append(title)
    # if resolution:
    #     new_name_parts.append(resolution)
    # if quality:
    #     new_name_parts.append(quality)
    # if languages_list:
    #     new_name_parts.append(languages_list)
    # new_name_parts.append(file_name.split('.')[-1])  # Keep the file extension
    
    # new_name = f"{season if season} • ".join(new_name_parts).strip()
    # return new_name

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def auto_rename(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    try:
        title = message.text
        # caption = file.caption
        print(f"title => {title}")
        print(f"file => {file}")
        # print(f"caption => {caption}")
    except Exception as e:
        print(e)
        pass
    new_file_name = rename_file(filename)
    await client.send_message(chat_id=message.from_user.id, text=f"📌Original: {filename} \n\n🤞Renamed: {new_file_name}")




# ===========================================================================
                    ### ./ AUTO RENAME = STEP 1
# ===========================================================================
# ===========================================================================




@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt=f"👋 Hey {user.mention} \nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ + ғɪʟᴇ ᴛᴏ ᴠɪᴅᴇᴏ ᴄᴏɴᴠᴇʀᴛᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴜᴘᴘᴏʀᴛ!\n\n♥ ʙᴇʟᴏᴠᴇᴅ ᴏᴡɴᴇʀ <a href='https://telegram.me/Simplifytuber2'>ʏᴀsʜ ɢᴏʏᴀʟ</a> 🍟"
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
        ],[
        InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs §', url='https://t.me/botupdatesimplifytuber'),
        InlineKeyboardButton('🍂 sᴜᴘᴘᴏʀᴛ §', url='https://t.me/bysimplifytuber')
        ],[
        InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ §', callback_data='about'),
        InlineKeyboardButton('ℹ ʜᴇʟᴘ §', callback_data='help')
        ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)


# @Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
# async def rename_start(client, message):
#     file = getattr(message, message.media.value)
#     filename = file.file_name
#     filesize = humanize.naturalsize(file.file_size) 
#     fileid = file.file_id
#     try:
#         text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
#         buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
#                    [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
#         await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
#         await sleep(FLOOD)
#     except FloodWait as e:
#         await sleep(e.value)
#         text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
#         buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
#                    [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
#         await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
#     except:
#         pass

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f"""👋 Hey {query.from_user.mention} \nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ + ғɪʟᴇ ᴛᴏ ᴠɪᴅᴇᴏ ᴄᴏɴᴠᴇʀᴛᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴜᴘᴘᴏʀᴛ!\n\n♥ ʙᴇʟᴏᴠᴇᴅ ᴏᴡɴᴇʀ <a href='https://telegram.me/Simplifytuber2'>ʏᴀsʜ ɢᴏʏᴀʟ</a> 🍟""",
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
                ],[
                InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs §', url='https://t.me/botupdatesimplifytuber'),
                InlineKeyboardButton('🍂 sᴜᴘᴘᴏʀᴛ §', url='https://t.me/bysimplifytuber')
                ],[
                InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ §', callback_data='about'),
                InlineKeyboardButton('ℹ ʜᴇʟᴘ §', callback_data='help')
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=mr.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=mr.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "dev":
        await query.message.edit_text(
            text=mr.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()





