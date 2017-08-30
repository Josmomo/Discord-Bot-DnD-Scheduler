import asyncio
import discord
from discord.ext import commands
import json

##### Setup #####
bot = commands.Bot(command_prefix='!', description='Schedule our adventures!')
amount = {}
member = discord.Member
server = discord.Server
default_data = {}
data = default_data
weekdays = {'1': 'Monday',
			'2': 'Tuesday',
			'3': 'Wednesday',
			'4': 'Thursday',
			'5': 'Friday',
			'6': 'Saturday',
			'7': 'Sunday'
}

##### Functions #####
# Load data
def loadData():
	global data
	global amount
	print("Loaded data:")
	with open('schedule_data.txt') as fp:
		data = json.load(fp)
		print(data)
	with open('amount.txt') as fp:
		amount = json.load(fp)
		print(amount)

# Save data
def saveData():
	global data
	global amount
	print("Saved data:")
	with open('schedule_data.txt', 'w') as fp:
		json.dump(data, fp)
		print(data)
	with open('amount.txt', 'w') as fp:
		json.dump(amount, fp)
		print(amount)

def checkPlayDays():
	s = ""
	for day in range(1,7):
		playableDay = False
		for key in list(data.keys()):
			if (data.get(key).count(str(day)) > 0):
				playableDay = True
			else:
				playableDay = False
				break
		if (playableDay):
			s += " " + weekdays.get(str(day))
	return s

##### Discord commands #####
@bot.event
async def on_ready():
	loadData()
	print(bot.user.name + ' is ready!')

@bot.event
async def on_message(message):
	global member
	global server
	member = message.author
	server = message.server
	await bot.process_commands(message)

@bot.command(name='hello', description='Test command.')
# Say hello
async def hello():
	await bot.say("Hello " + member.mention + "!")

@bot.command(name='add', description='Add days that you can play! Write !add <day_number>*')
# Add/update person
async def add(*args):
	global data
	name = member.name
	value = data.get(name, [])
	for i in range(0, len(args)):
		if (args[i].isdigit() and 0 < int(args[i]) and int(args[i]) < 8):
			value += args[i]
	value = list(set(value))
	value.sort()
	data.update({str(name):value})
	saveData()

	# Personal message
	message = member.mention + " can play on days:"
	for day in value:
		message += ' ' + weekdays.get(day)
	await bot.say(message)

	if (len(data) >= int(amount.get("amount"))):
		m = checkPlayDays()
		if (m != ""):
			await bot.say("@everyone Everyone can play on" + m + "!")

@bot.command(name='resetAll', description='Empties the whole schedule.')
# Description of command goes here
async def resetAll():
	global data
	if (member.server_permissions.administrator):
		data = default_data
		saveData()
		await bot.say("@everyone Schedule has been emptied for everyone! Time to sign up again!")

# !resättMäg
@bot.command(name='resetMe', description='Empties your schedule input.')
# Description of command goes here
async def resetMe():
	global data
	global member
	data.pop(member.name, None)
	saveData()
	await bot.say("Schedule has been emptied for " + member.mention + "!")

@bot.command(name='checkDay', description='List users that can play on that specified day')
# Description of command goes here
async def checkDay(*args):
	if (args[0].isdigit() and 0 < int(args[0]) and int(args[0]) < 8):
		m = "People availible to play on " + weekdays.get(args[0]) + ":"
		for key in list(data.keys()):
			if (data.get(key).count(args[0]) > 0):
				m += " " + str(key)
		await bot.say(m)

@bot.command(name='amount', description='Changes the amount of players required to play.')
# Description of command goes here
async def amount(*args):
	if (args[0].isdigit()):
		amount.update({"amount":args[0]})
		await bot.say("Amount of players needed changed to " + amount.get("amount") + "!")

#bot.run(BOT_TOKEN)