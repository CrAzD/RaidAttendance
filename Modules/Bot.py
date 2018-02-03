import discord

import asyncio
import configparser
import inspect
import math
import pickle
import os
import sys

from openpyxl import Workbook
from pathlib import Path
from threading import Thread

from discord.ext import commands
from .events import EventManager

class BotMain(commands.GroupMixin, discord.Client, discord.Server):
    def __init__(self, directory='', path={}, command_prefix='ra.', formatter=None, description=None, pm_help=True, **options):
        ## DEFAULT BOT START ##
        super().__init__(**options)
        self.command_prefix = command_prefix
        self.pm_help = pm_help
        self.command_not_found = options.pop('command_not_found', 'No command called "{}" found.')
        self.command_has_no_subcommands = options.pop('command_has_no_subcommands', 'Command {0.name} has no subcommands.')
        self._skip_check = discord.User.__ne__ if options.pop('self_bot', False) else discord.User.__eq__
        self.help_attrs = options.pop('help_attrs', {})
        self.help_attrs['pass_context'] = True
        if not 'name' in self.help_attrs:
            self.help_attrs['name'] = 'help'
        if not formatter is None:
            if not isinstance(formatter, commands.HelpFormatter):
                raise discord.ClientException('Formatter')
        ## DEFAULT BOT END ##


        self.events = {'counter':0, 'unparsed':{}}
        self.users = {}
        self.recordings = {}

        self.directory = directory
        self.path = path
        self.configs = {
            'general':self.config_initialize(file=self.path['config_general']),
            'permission':self.config_initialize(file=self.path['config_permission'])
        }
        self.token = self.configs['general']['SETUP']['Token']



    ### EVENTS ###



    ### GENERAL FUNCTIONS ###
    def config_initialize(self, file):
        if file.is_file():
            try:
                config_loaded = configparser.ConfigParser()
                config_loaded.read(file)
                return(config_loaded)
            except:
                print(f'Error:  Unable to read the config file. The sent file is {file}.')
                return(False)
        else:
            print(f'Error:  Unable to load the config file. The sent file path is {file}.')
            return(False)











class AttendanceBot(commands.GroupMixin, discord.Client, discord.Server, EventManager):
    def __init__(self, directory='', path={}, command_prefix='ra.', formatter=None, description=None, pm_help=True, **options):
        ## DEFAULT BOT START ##
        super().__init__(**options)
        self.command_prefix = command_prefix
        self.pm_help = pm_help
        self.command_not_found = options.pop('command_not_found', 'No command called "{}" found.')
        self.command_has_no_subcommands = options.pop('command_has_no_subcommands', 'Command {0.name} has no subcommands.')
        self._skip_check = discord.User.__ne__ if options.pop('self_bot', False) else discord.User.__eq__
        self.help_attrs = options.pop('help_attrs', {})
        self.help_attrs['pass_context'] = True
        if not 'name' in self.help_attrs:
            self.help_attrs['name'] = 'help'
        if not formatter is None:
            if not isinstance(formatter, commands.HelpFormatter):
                raise discord.ClientException('Formatter')
        ## DEFAULT BOT END ##

        self.events['counter'] = 0

        self.users = {}
        self.recordings = {}

        self.directory = directory
        self.path = path

        self.configs = {
            'general':self.config_initialize(file=self.path['config_general']),
            'permission':self.config_initialize(file=self.path['config_permission'])
        }

        self.server = None
        self.running = True
        self.token = self.configs['general']['SETUP']['Token']

        for perm in self.configs['permission']:
            if perm == 'DEFAULT':
                continue

            #for role in self.configs['commands'][command]['role_ids_with_access'].strip(" ").split(','):
            #    role = discord.utils.get(self.server.roles, id=role)
            #    print(role.id)
            #    print(role.name)

        """
        self.commands = {
            '_list':[],
            'recording_start':{
                'aliases':['rec_start', 'r_s', 'recstart', 'rs'],
                'function':self.recording_start,
                'permission_level':3,
                'valid_variables':{},
                'help_message':f'''
                '''
            },
            'recording_end':{
                'aliases':['rec_end', 'r_e', 'recend', 're'],
                'function':self.recording_end,
                'permission_level':3,
                'valid_variables':{},
                'help_message':f'''
                '''
            },
            'recording_list':{
                'aliases':['rec_list', 'r_l', 'reclist', 'rl'],
                'function':self.recording_list,
                'permission_level':3,
                'valid_variables':{},
                'help_message':f'''
                '''
            },
            'recording_get':{
                'aliases':['rec_get', 'r_g', 'recget', 'rg'],
                'function':self.recording_get,
                'permission_level':-1,
                'valid_variables':{},
                'help_message':f'''
                '''
            },
            'user_add':{
                'aliases':['u_a', 'ua', 'u+', 'user+'],
                'function':self.user_add,
                'permission_level':5,
                'valid_variables':{},
                'help_message':f'''
                '''
            },
            'user_remove':{
                'aliases':['u_r', 'ur', 'u-', 'user-'],
                'function':self.user_remove,
                'permission_level':5,
                'valid_variables':{},
                'help_message':f'''
                '''
            },
            'user_list':{
                'aliases':['u_l', 'ul', 'u|', 'user|'],
                'function':self.user_list,
                'permission_level':-1,
                'valid_variables':{},
                'help_message':f'''
                '''
            },
            'user_modify':{
                'aliases':['u_m', 'um', 'u=', 'user=', 'umod', 'usermod'],
                'function':self.user_modify,
                'permission_level':5,
                'valid_variables':{
                    'authorize': 'Boolean',
                    'admin': 'Boolean',
                    'name': 'String',
                    'excelfileonly': 'Boolean'
                },
                'help_message':f'''ra.user_modify allows you to manually adjust a users settings.

                Use Examples:
                    ra.user_modify targetid=################## excelfileonly=True
                    ra.user_modify targetid=################## authorize=True admin=False

                Valid Variables:  
                    authorize(Boolean), admin(Boolean), name(String), excelfileonly(Boolean)

                Aliases:
                    u_m, um, u=, user=, umod, usermod
                '''
            }
        }
        """



    ##EVENTS##
    async def on_ready(self):
        await self.channels_refresh()
        for record in self.recordings:
            if not record in self.channels:
                continue
            else:
                self.recordings.append(record)

        await print(self.user())
        self.loop.run_until_complete(self.loop_main)


    ##FUNCTIONS##
    async def loop_recording(self):
        while self.running:
            await self.event_loop()
            event = {
                'name':f'channels_refresh.{self.events["counter"]}',
                'async':True,
                'function':self.channels_refresh,
                'arguments':{}
            }
            self.events['counter'] += 1
            self.events['new'][event['name']] = event
            await asyncio.sleep(2.5)

    async def channels_refresh(self, args={}):
        self.channels = {}
        for channel in self.get_all_channels():
            if channel.id in self.channels:
                continue
            self.channels[channel.id] = channel
            if channel.name == '💤 AFriKa':
                print('################################################################')
                #print(channel.name)
                #print(channel.server)
                print(channel.id)
                #print(channel.topic)
                #print(channel.is_private)
                #print(channel.type)
                #print(channel.bitrate)
                print(channel.voice_members)
                #print(channel.user_limit)
                #print(channel.changed_roles)
                #print(channel.is_default)
                print(channel.mention)
                #print(channel.created_at)
                print(channel.overwrites)
                print('----------------------------------------------------------------')
                for mem in channel.voice_members:
                    print(mem.roles)
                    print(mem.status)
                    print(mem.top_role)
                    print(mem.server_permissions)
                    print(channel.permissions_for(mem))
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    for role in mem.roles:
                        print(role.id)
                        print(role.name)
                print('################################################################')

    async def str_to_bool(self, value):
        if str(value).lower() in ['true', 't', '1', 'yes', 'y', 'on', 'enable']:
            return(True)
        else:
            return(False)

    async def is_authorized(self, author, command='None', function_from='unknown'):
        cmd = command.lower()

        if not command or command == 'None':
            await self.send_message(author, f'ERROR:  No command was passed to is_authorized, sending function was {function_from}.')
            return(False)
        elif not cmd in self.Commands['_list']:
            await self.send_message(author, f'ERROR:  That command does **NOT** exist! You sent {command}, check your spelling.')
            return(False)
        elif not author.id in self.Users:
            await self.send_message(author, 'ERROR:  You have **NOT** been setup with this bot, speak with your system administrator.')
            return(False)
        elif not self.Users[author.id]['permission_level'] >= self.Commands[cmd]['permission_level'] and self.Commands[cmd]['permission_level'] != -1:
            await self.send_message(author, f'ERROR:  You are **NOT** authorized to use the ra.{cmd.upper()[:1]}{cmd[1:]} command.')
            return(False)
        else:
            return(True)

    def config_initialize(self, file):
        if file.is_file():
            try:
                config_loaded = configparser.ConfigParser()
                config_loaded.read(file)
                return(config_loaded)
            except:
                print(f'Error:  Unable to read the config file. The sent file is {file}.')
                return(False)
        else:
            print(f'Error:  Unable to load the config file. The sent file path is {file}.')
            return(False)

    def db_save(self, file):
        try:
            with open(file, 'wb') as file:
                pickle.dump(self.data, file, pickle.HIGHEST_PROTOCOL)
            return(True)
        except:
            return(False)
            self.channels[channel.name] = channel



    ##COMMANDS##
    @commands.command(name='recording_start', aliases=['rec_start', 'r_s', 'recstart', 'rs'])
    async def recording_start(self, ctx, channel_id: str=None):
        print(ctx)
        print(channel_id)
        """
        """
        if not self.is_authorized(message.author, 'recording_start'):
            return

        message_split = message.content.strip('ra.recording_start').split(" ")
        channel_ID = ''
        if '=' in message_split[0]:
            channel_ID = message_split[0].split('=')[1]
        else:
            channel_ID = message_split[0]

        found = True
        if not channel_ID in self.channels:
            await self.channels_refresh()
            if not channel_ID in self.channels:
                found = False
                await bot.send_message(message.author, f'ERROR: Channel ID  [{channel_ID}]  was not found.')

        if found:
            channel = self.channels[channel_ID]
            if channel.id in self.data['Recording'] or self.recording:
                await bot.send_message(message.author, ('ERROR: Unable to start recording as one is already running on that channel.'))
            else:
                t = datetime.now()
                self.recording[channel.id] = channel
                self.data['Recording'][channel.id] = {
                    'uniqueID': f'{channel.id}...{t.strftime("%H:%M:%S")}...{t.strftime("%Y-%m-%d")}',
                    'timeStart': t.strftime('%H:%M:%S'),
                    'timeEnd': 'Null:Null:Null',
                    'dateStart': t.strftime('%Y-%m-%d'),
                    'dateEnd': 'Null-Null-Null',
                    'Duration': 0,
                    'Comments': {},
                    'Members:': {}
                }

                await self.db_save()
                await self.send_message(message.author, (f'Recording STARTED in {channel.name}.\n\tuID={data["Recording"][channel.id]["uID"]}'))

    async def recording_end(self, message):
        author = message.author
        message_split = message.content.split(" ")

        channel_ID = ''
        if '=' in message_split[0]:
            channel_ID = message_split[0].split('=')[1]
        else:
            channel_ID = message_split[0]

        found = True
        if not channel_ID in self.channels:
            await self.channels_refresh()
            if not channel_ID in self.channels:
                found = False
                await bot.send_message(author, f'ERROR: Channel ID  [{channel_ID}]  was not found.')

        if found:
            if not channel_ID in data['Recording'] or not channel_ID in self.Recording:
                await bot.send_message(author, (f'FAILURE: Unable to end recording as one is not currently running in {channel.name}'))
                return(False)

            t = datetime.now()
            textPath = Path(f'{self.DIRECTORY}\\TextFiles\\{self.data["Recording"][channel.id]["uniqueID"].replace(":", ";")}.txt')
            textFile = open(textPath, 'w+', encoding='utf-8')

            channel_data = data['Recording'][channel.id]
            channel_data['timeEnd'] = t.strftime('%H:%M:%S')
            channel_data['dateEnd'] = t.strftime('%Y-%m-%d')
            channel_data['Message'] = {'Count': 0,
            0: f'''{channel.name}
                    Started:  {channel_data['timeStart']}, {channel_data['dateStart']}
                    Ended:  {channel_data['timeEnd']}, {channel_data['dateEnd']}
                    Duration:  {channel_data['Duration']} total seconds || {math.ceil(channel_data['Duration']/60)} Minutes *Rounded Up*.
                    Unique ID:  {channel_data['uniqueID']}
            '''
            }

            for member in channel.voice_members:
                mem = self.data['Recording'][channel.id]['Members'][member.id]
                mem['timeEnd'] = channel_data['timeEnd']
                mem['dateEnd'] = channel_data['dateEnd']

            for member in channel_data['Members']:
                mem = channel_data['Members'][member]
                mess = f'''
                {mem['name']}
                        ID: {member}
                        Joined: {mem['timeJoined']}, mem['dateJoined']
                        Ended:
                '''
                if len(mess) + len(channel_data['Message']['Count']) > 2000:
                    channel_data['Message']['Count'] += 1
                    channel_data['Message'][channel_data['Message']['Count']] = mess
                else:
                    channel_data['Message'][channel_data['Message']['Count']] += mess

            textFile.write(mess)
            textFile.close()

            #Max length of a message is 2,000 characters.
            if not self.data['Users'][author.id]['textFileOnly']:
                i = 0
                while i < channel_data['Message']['Count']:
                    try:
                        await self.send_message(author, channel_data['Message'][i])
                    except:
                        pass
                    i += 1

            #Send textFile over to person who ended the recording.
            await self.send_file(message.author, textPath, filename=(f'{data["recording"][channel.id]["uniqueID"].replace(":", ";").txt}'))
            del self.recording[channel.id]
            del self.data['Recording'][channel.id]
            await self.db_save()

    async def recording_list(self):
        print('Create the recording_list function')

    async def recording_get(self):
        print('Create the recording_get function')

    async def user_add(self):
        print('Create the user_add function')

    async def user_remove(self):
        print('Create the user_remove function')

    async def user_modify(self, target, message_split):
        author = message.author

        for message in message_split:
            correct = True

            if not '=' in message:
                await self.send_message(author, f'''ERROR:  Missing the = sign, or space seperation.
                    {message}''')
                correct = False

            try:
                message_split2 = message.split('=')
                key = message_split2[0]
                value = message_split2[1]
            except:
                await self.send_message(author, f'''ERROR:  Syntax error.
                    {message}''')
                correct = False
            
            #FIX THIS#
            if not key in self.Commands['user_modify']['valid_variables']:
                await self.send_message(author, f'''ERROR:  Unknown variable entered.
                    You sent: "{message}"
                ''')
                correct = False

            if not correct:
                await self.help_manual(author, 'user_modify')
                continue

            try:
                if not target.id in self.data['Users']:
                    self.data['Users'][target.id] = {
                        'Admin': False,
                        'Authorized': False,
                        'Name': target.name,
                        'fileOnly': False
                    }

                if self.data['Default']['Keys'][key] == 'Boolean':
                    value = self.str_to_bool(value)

                self.data['Users'][target.id][key] = Value
                await db_save()
                await self.send_message(author, f'{target.name}\'s {key.upper()} setting has been set to {str(value.upper())}.')
                continue
            except discord.NotFound:
                await self.send_message(author, f'ERROR: The UniqueID ({uID}) was not found in discord\'s database.')
                continue
            except discord.HTTPException:
                await self.send_message(author, f'ERROR: HTTP failure when pulling UniqueID ({uID}).')
                continue

    async def user_list(self, author):
        await self.send_message(author, f'Users in database')
        for uniqueID in self.Users:
            try:
                await self.send_message(author, f'''
                    {self.Users[uniqueID]["Name"]}:
                        UniqueID:  {uniqueID}
                        Permission Level: {self.Users[uniqueID]["permission_level"]}
                ''')
            except:
                continue