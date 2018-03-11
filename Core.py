import discord

from pathlib import Path

from modules.bot import AttendanceBot, BotMain

#Setup the dictionary for the bot init
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PATH = {
    'config':Path(DIRECTORY+'\\Config'),
    'data':Path(DIRECTORY+'\\Data'),
    'logs':Path(DIRECTORY+'\\Logs'),
    'modules':Path(DIRECTORY+'\\Modules'),
    'other':Path(DIRECTORY+'\\Other'),
    'config_general':Path(DIRECTORY+'\\Config\\General.ini'),
    'config_permission':Path(DIRECTORY+'\\Config\\Permission.ini')
}
#b = BotMain(directroy=DIRECTORY, path=PATH)
Bot = AttendanceBot(directroy=DIRECTORY, path=PATH)
Bot.run(Bot.token)


'''
https://github.com/Rapptz/discord.py/blob/rewrite/discord/ext/commands/core.py
https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/utils/checks.py

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
'''