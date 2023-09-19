 from info import *
from utils import *
from client import User 
from pyrogram import Client, filters

@Client.on_message(filters.group & filters.command("connect"))
async def connect(bot, message):
    m=await message.reply("connecting..")
    user = await User.get_me()
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
       channels  = group["channels"].copy()
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Only {user_name} ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ 😁")
    if bool(verified)==False:
       return await m.edit("Tʜɪs ᴄʜᴀᴛ ɪs ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nᴜsᴇ /verify")    
    try:
       channel = int(message.command[-1])
       if channel in channels:
          return await message.reply("Tʜɪs ᴄʜᴀɴɴᴇʟ ɪs ᴀʟʀᴇᴀᴅʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ! Yᴏᴜ Cᴀɴᴛ Cᴏɴɴᴇᴄᴛ Aɢᴀɪɴ")
       channels.append(channel)
    except:
       return await m.edit("❌ Iɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ!\nᴜsᴇ `/connect CʜᴀɴɴᴇʟID`")    
    try:
       chat   = await bot.get_chat(channel)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link
       await User.join_chat(c_link)
    except Exception as e:
       if "Tʜᴇ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ" in str(e):
          pass
       else:
          text = f"❌ Error: `{str(e)}`\nMᴀᴋᴇ sᴜʀᴇ I'ᴍ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ & ᴛʜɪs ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs ᴀɴᴅ {(user.username or user.mention)} ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ ᴛʜᴇʀᴇ"
          return await m.edit(text)
    await update_group(message.chat.id, {"channels":channels})
    await m.edit(f"✅ Sᴜᴄᴄᴇssғᴜʟʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#NewConnection\n\nUser: {message.from_user.mention}\nɢʀᴏᴜᴘ: [{group.title}]({g_link})\nCʜᴀɴɴᴇʟ: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_message(filters.group & filters.command("disconnect"))
async def disconnect(bot, message):
    m=await message.reply("Pʟᴇᴀsᴇ ᴡᴀɪᴛ..")   
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
       channels  = group["channels"].copy()
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Only {user_name} ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ 😁")
    if bool(verified)==False:
       return await m.edit("Tʜɪs ᴄʜᴀᴛ ɪs ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nᴜsᴇ /verify")    
    try:
       channel = int(message.command[-1])
       if channel not in channels:
          return await m.edit("Yᴏᴜ ᴅɪᴅɴ'ᴛ ᴀᴅᴅᴇᴅ ᴛʜɪs ᴄʜᴀɴɴᴇʟ ʏᴇᴛ Oʀ Cʜᴇᴄᴋ CʜᴀɴɴᴇʟIᴅ")
       channels.remove(channel)
    except:
       return await m.edit("❌ Iɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ!\nᴜsᴇ `/disconnect CʜᴀɴɴᴇʟIᴅ`")
    try:
       chat   = await bot.get_chat(channel)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link
       await User.leave_chat(channel)
    except Exception as e:
       text = f"❌ Error: `{str(e)}`\nMᴀᴋᴇ sᴜʀᴇ I'ᴍ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ & ᴛʜɪs ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs ᴀɴᴅ {(user.username or user.mention)} ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ ᴛʜᴇʀᴇ"
       return await m.edit(text)
    await update_group(message.chat.id, {"channels":channels})
    await m.edit(f"✅ Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴄᴏɴɴᴇᴄᴛᴇᴅ ғʀᴏᴍ [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#DisConnection\n\nUser: {message.from_user.mention}\nGʀᴏᴜᴘ: [{group.title}]({g_link})\nCʜᴀɴɴᴇʟ: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_message(filters.group & filters.command("connections"))
async def connections(bot, message):
    group     = await get_group(message.chat.id)    
    user_id   = group["user_id"]
    user_name = group["user_name"]
    channels  = group["channels"]
    f_sub     = group["f_sub"]
    if message.from_user.id!=user_id:
       return await message.reply(f"Only {user_name} ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ 😁")
    if bool(channels)==False:
       return await message.reply("Tʜɪs ɢʀᴏᴜᴘ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ᴄʜᴀɴɴᴇʟs!\nCᴏɴɴᴇᴄᴛ ᴏɴᴇ ᴜsɪɴɢ /connect")
    text = "Tʜɪs Gʀᴏᴜᴘ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ:\n\n"
    for channel in channels:
        try:
           chat = await bot.get_chat(channel)
           name = chat.title
           link = chat.invite_link
           text += f"🔗Cᴏɴɴᴇᴄᴛᴇᴅ Cʜᴀɴɴᴇʟ - [{name}]({link})\n"
        except Exception as e:
           await message.reply(f"❌ Eʀʀᴏʀ ɪɴ `{channel}:`\n`{e}`")
    if bool(f_sub):
       try:
          f_chat  = await bot.get_chat(channel)
          f_title = f_chat.title
          f_link  = f_chat.invite_link
          text += f"\nFSub: [{f_title}]({f_link})"
       except Exception as e:
          await message.reply(f"❌ Eʀʀᴏʀ ɪɴ Fsᴜʙ (`{f_sub}`)\n`{e}`")
   
    await message.reply(text=text, disable_web_page_preview=True)
