
from telebot.async_telebot import AsyncTeleBot
from module.playstore import *
from datetime import datetime

BOT_TOKEN = '6695550712:AAGWiGF4DGxMGsAhp1o7c25xWJWlltS0LvI'
bot = AsyncTeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
	await bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
async def echo_all(message):
	package_name = message.text
	app_infos = await get_play_store(package_name)
	fmt = app_infos['updated'].replace(',', '').replace('Sept', 'Sep')
	dt = datetime.strptime(fmt, "%d %b %Y")
	formated = dt.strftime("%d/%m/%Y")
	
	d1 = datetime.strptime(formated, "%d/%m/%Y")
	d2 = datetime.strptime(datetime.today().strftime("%d/%m/%Y"), "%d/%m/%Y")
	dx = d2 - d1



	rep = f'''
<b>App name</b>: <a href="https://play.google.com/store/apps/details?id={package_name}&hl=en_GB&gl=us">{app_infos['name']}</a>
<b>Category</b>: {app_infos['category']}
<b>Publisher</b>: <a href="{app_infos['store']}">{app_infos['publisher']}</a>
<b>Version</b>: {app_infos['version']}
<b>Total installs</b>: {app_infos['totalinstalls']}
<b>Rating</b>: {app_infos['rating']} &#9733; ( {app_infos['numrating']} reviews )
<b>Friendly</b>: {app_infos['friendly']}
<b>Updated</b>: {app_infos['updated']} ({dx.days} days ago)
<b>Published</b>: {app_infos['published']}
<b>Support email</b>: {app_infos['email']}
	'''
	await bot.send_message(message.chat.id, rep)
	# await bot.reply_to(message, rep)

import asyncio
asyncio.run(bot.polling())
