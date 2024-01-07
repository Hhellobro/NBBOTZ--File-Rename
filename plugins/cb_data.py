from helper.progress import progress_for_pyrogram, TimeFormatter

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import *
import os
import random
from PIL import Image
import time
from datetime import timedelta
from helper.ffmpeg import take_screen_shot, fix_thumb
from helper.progress import humanbytes
from helper.set import escape_invalid_curly_brackets
import os

log_channel = int(os.environ.get("LOG_CHANNEL", ""))

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

STRING = os.environ.get("STRING", "")

ADMIN = os.environ.get("ADMIN", "")

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=STRING)


@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        return


@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    date_fa = str(update.message.date)
    pattern = '%Y-%m-%d %H:%M:%S'
    date = int(time.mktime(time.strptime(date_fa, pattern)))
    chat_id = update.message.chat.id
    id = update.message.reply_to_message_id
    await update.message.delete()
    await update.message.reply_text(f"__Please enter the new filename...__\n\nNote:- Extension Not Required", reply_to_message_id=id,
                                    reply_markup=ForceReply(True))
    dateupdate(chat_id, date)


@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    date = used_["date"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("Trying To Download...")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=(" Trying To Download...",  ms, c_time))

    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    user_id = int(update.message.chat.id)
    data = find(user_id)
    try:
        c_caption = data[1]
    except:
        pass
    thumb = data[0]
    if c_caption:
        doc_list = ["filename", "filesize"]
        new_tex = escape_invalid_curly_brackets(c_caption, doc_list)
        caption = new_tex.format(
            filename=new_filename, filesize=humanbytes(file.file_size))
    else:
        caption = f"**{new_filename}**"
    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        c_time = time.time()

    else:
        ph_path = None

    value = 2090000000
    if value < file.file_size:
        await ms.edit("Trying To Uploade.....")
        try:
            filw = await app.send_document(log_channel, document=file_path, thumb=ph_path, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```",  ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                pass
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                return
    else:
        await ms.edit("Trying To Upload....")
        c_time = time.time()
        try:
            await bot.send_document(update.from_user.id, document=file_path, thumb=ph_path, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            return


@Client.on_callback_query(filters.regex("vid"))
async def vid(bot, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    date = used_["date"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("Trying To Download...")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("``` Trying To Download...```",  ms, c_time))

    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    user_id = int(update.message.chat.id)
    data = find(user_id)
    try:
        c_caption = data[1]
    except:
        pass
    thumb = data[0]

    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    if c_caption:
        vid_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(
            file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"
    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        c_time = time.time()

    else:
        try:
            ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
            width, height, ph_path = await fix_thumb(ph_path_)
        except Exception as e:
            ph_path = None
            print(e)

    value = 2090000000
    if value < file.file_size:
        await ms.edit("Trying To Upload.....")
        try:
            filw = await app.send_video(log_channel, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```",  ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                pass
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                return
    else:
        await ms.edit("Trying To Upload....")
        c_time = time.time()
        try:
            await bot.send_video(update.from_user.id, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            return


@Client.on_callback_query(filters.regex("aud"))
async def aud(bot, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    ms = await update.message.edit("Trying To Download...")
    c_time = time.time()
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("``` Trying To Download...```",  ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    user_id = int(update.message.chat.id)
    data = find(user_id)
    c_caption = data[1]
    thumb = data[0]
    if c_caption:
        aud_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, aud_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(
            file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        await ms.edit("Trying To Upload...")
        c_time = time.time()
        try:
            await bot.send_audio(update.message.chat.id, audio=file_path, caption=caption, thumb=ph_path, duration=duration, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
            os.remove(ph_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            os.remove(ph_path)
    else:
        await ms.edit("Trying To Upload.....")
        c_time = time.time()
        try:
            await bot.send_audio(update.message.chat.id, audio=file_path, caption=caption, duration=duration, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```",  ms, c_time))
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            await ms.edit(e)
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            os.remove(file_path)
    
  elif data == "help":
        await query.message.edit_text(
            text=Translation.HELP_TXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
                 [[
                 InlineKeyboardButton('👨🏻 Owner commands', callback_data="owner_cmd"),
                 InlineKeyboardButton('💬 About', callback_data="about")
                 ],[
                 InlineKeyboardButton('back', callback_data="start")
            ]]
        ))
        
    elif data == "owner_cmd":
        await query.message.edit_text(
            text=Translation.OWNER_COMMANDS_TXT,
            reply_markup=InlineKeyboardMarkup(
               [[InlineKeyboardButton('Back', callback_data="help")]]
        ))
     
    elif data == "about":
        await query.message.edit_text(
            text=Translation.ABOUT_TXT.format(client.me.first_name, client.me.username,
                                             __version__, bot_version),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [[
              InlineKeyboardButton('📃 Source code', url='https://github.com/Greymattersbot/md-renamebot')
            ],[
              InlineKeyboardButton('Back', callback_data = "help"),
            ]]
        ))
     
    elif data in ['settings', 'toggle_mode']:
       mode = await db.get_uploadmode(user_id)
       if data == "toggle_mode":
          if not mode:
             mode = "document"
          elif mode == "document":
             mode = "video"
          elif mode == "video":
             mode = "audio"
          else:
             mode = None 
          await db.change_uploadmode(user_id, mode)
       button = [[
         InlineKeyboardButton('📝 Custom Caption', callback_data="custom_caption")
         ],[
         InlineKeyboardButton('🖼️ Custom Thumbnail', callback_data="custom_thumbnail")
         ],[
         InlineKeyboardButton(f'📤 Upload mode', callback_data="toggle_mode"),
         InlineKeyboardButton(mode if mode else "Default", callback_data="toggle_mode")
         ],[
         InlineKeyboardButton('⛔ Close', callback_data="close")
         ]] 
       await query.message.edit_text(
          text=Translation.SETTINGS_TXT,
          reply_markup=InlineKeyboardMarkup(button))
        
    elif data == "custom_caption":
        await query.message.edit_text(
            text=Translation.CUSTOM_CAPTION_TXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
              [[
                InlineKeyboardButton('👀 Show Caption', callback_data="show_caption"),
                InlineKeyboardButton("🗑️ Delete Caption", callback_data="delete_caption")
              ],[
                InlineKeyboardButton('Back', callback_data="settings")
              ]]
        ))
             
    elif data =="show_caption":
        caption = await db.get_caption(user_id)
        if not caption:
           return await query.answer("You didn't added any custom caption", show_alert=True)
        await query.answer(f"Your Custom Caption:\n\n{caption}", show_alert=True)
        
    elif data == "delete_caption":
        caption = await db.get_caption(user_id)
        if not caption:
           return await query.answer("Nothing will found to delete", show_alert=True)
        await db.set_caption(query.from_user.id, None)
        return await query.answer("caption deleted successfully", show_alert=True)   
    
    elif data == "custom_thumbnail":
        await query.message.edit_text(
            text=Translation.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton('👀 Show Thumbnail', callback_data="show_thumb"),
                InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="delete_thumb")
                ],[
                InlineKeyboardButton('Back', callback_data="settings")
               ]]
        ))
        
    elif data == "show_thumb":
        thumb = await db.get_thumbnail(user_id)
        if not thumb:
           return await query.answer(Translation.THUMB_NOT_FOUND_TXT, show_alert=True)
        await query.message.delete()
        await query.message.reply_photo(thumb)
            
    elif data == "delete_thumb":
        thumb = await db.get_thumbnail(user_id)
        if not thumb:
           return await query.answer(Translation.THUMB_NOT_FOUND_TXT, show_alert=True)
        await db.set_thumbnail(user_id, None)
        return await query.answer(Translation.REMOVE_CUSTOM_THUMB_TXT, show_alert=True)
        
    
# 
#  LazyDeveloperr
# 
