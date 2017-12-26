import discord

import asyncio
import configparser
import inspect
import math
import pickle
import os
import sys

config = configparser.ConfigParser()
config.sections()

from discord.ext.commands.core import GroupMixin, Command, command
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandNotFound, CommandError
from discord.ext.commands.formatter import HelpFormatter
from discord.ext import commands

from datetime import datetime
from pathlib import Path

#from Modules.Bot import Bot as Bot

class Bot(object):
	def __init__(self):
		print('hello')


#SETUP THE BOT
Bot.DIRECTORY = os.path.dirname(os.path.abspath(__file__))
Bot.PATH_CONFIG = Bot.DIRECTORY+'\\Config'
Bot.PATH_DATA = Bot.DIRECTORY+'\\Data'
Bot.PATH_LOGS = Bot.DIRECTORY+'\\Logs'
Bot.PATH_MODULES = Bot.DIRECTORY+'\\Modules'
Bot.PATH_OTHER = Bot.DIRECTORY+'\\Other'
Bot.PATH_TOKEN = Path(Bot.PATH_CONFIG + '\\TOKEN.TOKEN')

Bot.CONFIG_TOKEN = (configparser.ConfigParser().sections()).read(Bot.PATH_TOKEN)

#LOAD THE TOKEN FROM THE TOKEN.TOKEN FILE IN THE CONFIG FOLDER!
if not Bot.PATH_TOKEN.is_file():
	print(f'ERROR:  TOKEN.TOKEN file was NOT found in the {Bot.PATH_CONFIG} folder.')

else:
	#Bot.TOKEN = Bot.CONFIG_TOKEN['TOKEN']['TOKEN']
	#print(config['TOKEN']['TOKEN'])
	print(Bot.CONFIG_TOKEN)
	#print('#####################################################')
	#print(config.read(Path(Bot.PATH_CONFIG + '\\TOKEN2.TOKEN')))

	#print(lines)
	#Bot.Run

'''

#GLOBALS
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PICKLE_PATH = DIRECTORY+'\\BotRaidAtendanceInfo.pickle'
PICKLE_FILE = Path(PICKLE_PATH)


#DATABASE
	#Creation
	#Loading
	#Structure of an individual Recording
		"""
			'Recording':{
				'333733237203664898':{
				'uID':'333733237203664898+Date+StartTime',
				'TimeStart':5,
				'TimeEnd':8999595,
				'DateStart':7242017,
				'DateEnd':7252017,
				'Duration':12, #Duration of recording in seconds.
				'Comments':{},
				'Members':{
					'95620119144697856':{
						'Name':'CrAzD',
						'TimeJoined':{
							0:123,
							1:123,
						}
						'TimeJoined':1205,
						'TimeLeft':1305,
						'DateJoined':7252017,
						'DateLeft':7262017,
						'Duration':12,
						'Comments':{}
					}
				}
			}
		"""
if not PICKLE_FILE.is_file():
	data = {
		'Perms':{
			'95624419354873856':True,
			'95620119144697856':True
		},
		'Names':{
			'95624419354873856':'Aumz',
			'95620119144697856':'CrAzD'
		},
		'Recordings':{}
	}
	with open(PICKLE_FILE, 'wb') as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
else:
	with open(PICKLE_FILE, 'rb') as file:
		data = pickle.load(file)

Bot.PICKLE_FILE = PICKLE_FILE



#EVENTS
@Bot.event
async def on_ready():
	await Bot.channels_refresh()

	for recording in data['Recordings']:
		if not recording in Bot.channels:
			continue

		Bot.recordings[recording] = channel

	Bot.loop.create_task(Bot.loop_recording())


@Bot.event
async def on_message(message):
	if message.author != Bot.user and message.content.startswith('ra.'):

		for cmd in COMMAND_LIST:
			if not message.content.startswith(f'ra.{cmd}'):
				continue

			command = cmd
			message.content = message.content.replace(command, "", 1)

			FUNCTIONS[command](message)
			break

	try:
		await bot.process_commands(message)
	except AttributeError:
		pass



Bot.run('TOKEN-GOES-HERE')
'''