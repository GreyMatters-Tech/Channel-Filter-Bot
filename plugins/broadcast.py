import asyncio
from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.errors import FloodWait


@Client.on_message(filters.command('broadcast') & filters.user(ADMIN))
async def broadcast(bot, message):
    if not message.reply_to_message:
       return await message.reply("Use this command as a reply to any message!")
    m=await message.reply("Broadcasting...")   

    count, users = await get_users()
    stats     = "⚡ Broadcast Processing.."
    br_msg    = message.reply_to_message
    total     = count       
    remaining = total
    success   = 0
    failed    = 0    
     
    for user in users:
        chat_id = user["_id"]
        trying = await copy_msgs(br_msg, chat_id)
        if trying==False:
           failed+=1
           remaining-=1
        else:
           success+=1
           remaining-=1
        try:                                     
           await m.edit(script.BROADCAST.format(stats, total, remaining, success, failed))                                 
        except:
           pass
    stats = "✅ Broadcast Completed"
    await m.reply(script.BROADCAST.format(stats, total, remaining, success, failed)) 
    await m.delete()                                


async def copy_msgs(br_msg, chat_id):
    try:
       await br_msg.copy(chat_id)       
    except FloodWait as e:
       await asyncio.sleep(e.value)
       await copy_msgs(br_msg, chat_id)
    except: 
       return False      
