"""lokaman"""
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from pyrogram import Client , filters

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
	text = """**Free Plan User**
	Daily  Upload limit 1.2GB
	Price 0
	
	** Silver Plan ** 
	Daily  Upload  limit 10GB
	Price Rs 20 Per Month
	
	** Gold Plan**
	Daily Upload limit 50GB
	Price Rs 50 Per Month
	
	** Diamond Plan**
	Daily Upload limit 100GB
	Price Rs 80 Per Month
	
	After Payment Send Screenshots To Admin
        """
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("ADMIN ",url = "https://t.me/Bot0987654")], 
        			[InlineKeyboardButton("Paytm",url = "https://p.paytm.me/xCTH/vo37hii9"),
        			InlineKeyboardButton("Paytm",url = "https://p.paytm.me/xCTH/vo37hii9")],[InlineKeyboardButton("Cancel",callback_data = "cancel")  ]])
	await update.message.edit(text = text,reply_markup = keybord)
	

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot,message):
	text = """**Free Plan User**
	Daily  Upload limit 1.2GB
	Price 0
	
	** Silver Plan ** 
	Daily  Upload  limit 10GB
	Price Rs 20 Per Month
	
	** Gold Plan**
	Daily Upload limit 50GB
	Price Rs 50 Per Month
	
	** Diamond Plan**
	Daily Upload limit 100GB
	Price Rs 80 Per Month
	
	After Payment Send Screenshots To Admin"""
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("ADMIN ",url = "https://t.me/Bot0987654")], 
        			[InlineKeyboardButton("Paytm",url = "https://p.paytm.me/xCTH/vo37hii9"),
        			InlineKeyboardButton("Paytm",url = "https://p.paytm.me/xCTH/vo37hii9")],[InlineKeyboardButton("Cancel",callback_data = "cancel")  ]])
	await message.reply_text(text = text,reply_markup = keybord)
