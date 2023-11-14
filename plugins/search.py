import asyncio
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

# Bot Client for Inline Search
Bot = Client(
    session_name=info.SESSION,
    api_id=info.API_ID,
    api_hash=info.API_HASH,
    bot_token=info.BOT_TOKEN
)

# User Client for Searching in Channel.
User = Client(
    session_name=info.SESSION,
    api_id=info.API_ID,
    api_hash=info.API_HASH
)

@Bot.on_message(filters.incoming)
async def inline_handlers(_, event: Message):
    if event.text == '/start':
        return
    answers = f'**Searching For "{event.text}" 🔍**'
    async for message in User.search_messages(chat_id=info.CHANNELS, limit=50, query=event.text):
        if message.text:
            thumb = None
            f_text = message.text
            msg_text = message.text.html
            if "|||" in message.text:
                f_text = message.text.split("|||", 1)[0]
                msg_text = message.text.html.split("|||", 1)[0]
            answers += f'**🍿 Title ➠ ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n📜 About ➠ ' + '' + f_text.split("\n", 2)[-1] + ' \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\nLink Will Auto Delete In 60Sec...⏰\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    try:
        msg = await event.reply_text(answers)
        await asyncio.sleep(60)
        await event.delete()
        await msg.delete()
    except:
        print(f"[{info.SESSION}] - Failed to Answer - {event.from_user.first_name}")


# Start Clients
Bot.start()
User.start()
# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
User.stop()
