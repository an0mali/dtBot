# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 22:28:16 2021

@author: Qui
"""

import asyncio
from asyncio.windows_events import NULL
import discord
import os
import time

from requests.api import delete
import botutils
import authkey
from discord.ext import commands
import threading
from pathlib import Path
from random import randint
from Pycom import pycom

class dtBot(object):
        
    def __init__(self, name, *kwargs):
        self.name = name
        intents = discord.Intents.default()
        intents.members = True
        activity = discord.Game(name='Ultimate Turtle Simulator')
        self.bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)
        self.pycom = pycom.Pycom('a', self)
        self.outcoms = []
        self.prev_update_time = 0.0
        self.sigalrm_obj = ''
        self.chat_target = False
        self.humpty = botutils.BotUtils()
        self.authkey = authkey.authkey
        self.chk_nxt = False
        self.ctx_count = 1
        
        self.ctx_responses = {'all': []}
        self.ctx_objs = {}
        self.user_screens = {}
        self.new_user_screens = {}
        
        self.max_ctx_time = 180.0
        self.prev_checkctx_time = 0.0
        self.clear_ctx_wait = 90.0
        self.rm_usrscreen = []
        @self.bot.event
        async def on_member_join(member):
            print('Member join detected')
            for channel in self.bot.get_all_channels():
                if channel.name == 'general-chat':
                    await channel.send(f'{member.mention} ', file=discord.File(Path('./textures/welcomepartner.png')))
                    return
                
        @self.bot.event
        async def on_ready():
            print('Bot connected')
            

        @self.bot.listen('on_message')
        async def on_message(message):
            if message.author == self.bot.user:
                return
                
            if message.content.startswith('!'):
                
                print('Com detected.')
                return
                
        @self.bot.command(brief='Roast humpty', description='Refer to the breif description')
        async def roast(ctx, *args):
            print('bully com')
            print(ctx.author)
            await ctx.channel.send('humpty prolly doesnt even code ngl', file=discord.File(Path('./textures/garytriggered.gif')))
        
        @self.bot.command(brief='Post random gif')
        async def gifme(ctx):
                mpath = self.get_random_meme()
                await ctx.send('', file=discord.File(Path(mpath)))
                
        @self.bot.command(brief='Not a weeb? Use this', description="We be a weeb for you so you don't have to")
        async def weebs(ctx):
            mes = self.get_rand_quote('weebs')
            await ctx.send(mes)
        @self.bot.command(brief='Do not use this', description='Please do not use this')
        async def uwu(ctx):
            mes = self.get_rand_quote('uwu')
            await ctx.send(mes)            
        @self.bot.command(brief='Post random shit', description='The best way to be both interesting and funny without having to be either')
        async def shitpost(ctx):
            mes = self.get_shitpost()
            await ctx.send(mes)
            
        @self.bot.command(brief='Play UTS via discord. Super beta', description='Use normal uts commands, but !uts instead of !. Try !uts stats')
        async def uts(ctx, *args):
            if not len(args):
                await ctx.send(f'{ctx.author.mention}' + 'You must specifiy a command. Try !uts stats')
                return
            usrnm = ctx.author.name + '_discord'
            #emb = self.get_uts_embed()
            mesobj = await ctx.send('**Ultimate Turtle Simulator**\n Sending command "' + args[0] + '" to turtle "' + usrnm + '"')#, embed=emb)
            #time.sleep(0.1)
            ctxid = self.get_ctx_id(ctx, mesobj)
            com = '!' + usrnm + ',!'
            for arg in args:
                if arg != args[0]:
                    com += ' '
                com += arg
            com += ',' + ctxid
            print('Uts com received')
            self.pycom.send_toclient(com)
            time.sleep(0.1)
            #await self.check_feedback()

        @self.bot.command(brief='Meme me bruh')
        async def mememe(ctx):
            mem = 'Synchronizing memeographic resonance..'
            mesobj = await ctx.send(mem)
            failed = True
            attempts = 10
            for x in range(attempts):
                    mem = self.humpty.search_reddit()
                    if mem:
                        failed = False
                        break
                    #else:
                     #   failed = True
                      #  break
            
            if not failed:
                await ctx.send(mem)
                await mesobj.edit(content='Consider yourself memed')
            else:
               await mesobj.edit(content='Meme sychronization failed. You have died.')
                    
        @self.bot.command(brief='Get server member count')
        async def server_count(ctx):
            usrcount = self.get_total_users(ctx)
            await ctx.send('Total number of weebs in server: ' + str(usrcount -1))

        @self.bot.command(brief='About this bot')
        async def about(ctx):
            embed = discord.Embed(
                title='Go here NOW',
                url = 'https://derangedturtlegames.com',
                description = 'v0.69420 made by Jesus H Fucking Christ and a paperclip'
                )
            ico = 'https://static.wixstatic.com/media/e7a94e_0cb9088f334a4392901aeeb04c47f884~mv2.png'
            auth = 'Deranged Turtlebot'
            if not randint(0,5):
                auth = 'Jesus H Fucking Christ'
                ico = 'https://i.pinimg.com/originals/31/b8/f6/31b8f6c73de6fa6eee96f0c6545d6de4.jpg'
            embed.set_author(
                name=auth,
                url='https://twitter.com/_dtgames',
                icon_url= ico
                )
            await ctx.send(embed=embed)
        self.run_bot()

    def send_to(self, mes, ctxid, utsres=False):
        #print('Sending: ' + mes + ' to ' + ctxid)
        #create_task(self.send_message(mes, ctxid))
        #self.bot.loop.create_task(self.send_message(mes, ctxid, utsres))
        self.bot.loop.create_task(self.send_message(mes, ctxid, utsres))
        #self.bot.loop.run_until_complete(self.send_message(mes, ctxid, utsres))

    async def send_message(self, mes, ctxid, uts_response=False):
        #print('Send message:: Sending message to CTXID:"' + ctxid + '"')
        if ctxid == 'all':
            for channel in self.bot.get_all_channels():
                if channel.name == 'uturtle-bot-dev':
                    await channel.send(mes)
                    break
        else:
            if ctxid in self.ctx_objs:
                ctxdata = self.ctx_objs[ctxid]
                chan_name = ctxdata['channel_name']
                ctxobj = ctxdata['channel']
                for channel in self.bot.get_all_channels():
                    if channel.name == chan_name:
                        ctxobj = channel
                mes = self.format_uts_mes(mes, ctxdata['auth_name'])
                mes = '\n' + mes
                title = ''
                mention = ctxdata['auth_mention']
                if not uts_response:
                    await ctxobj.send(title + f'{mention}' + mes)
                else:
                    title = '**Ultimate Turtle Simulator** '
                    oldmesobj = False
                    efile = False
                    authname = ctxdata['auth_name'] + '_discord'
                    print('Authname is ' + authname)
                    sdat = False
    
                    if authname in self.user_screens:
                        print('Found authname')
                        if len(self.user_screens[authname]):
                            sdat = self.user_screens[authname].pop(-1)
                            
                            #self.rm_usrscreen[authname] = sdat
                            rawpath = sdat[0]
                            try:
                                self.rm_usrscreen.append(rawpath)
                                epath = os.path.expandvars(rawpath)
                                print('Epath is ' + str(epath))
                                efile = True
                            except:
                                pass
                    else:
                        print('Current userscreens: ' + str(self.user_screens))
                        #print('Epath is ' + str(epath))
                        #efile = discord.File(Path(epath))

                    if self.ctx_objs[ctxid]['mesobj']:
                        oldmesobj = self.ctx_objs[ctxid]['mesobj']
                        
                        self.ctx_objs[ctxid]['mesobj'] = False

                    if efile:
                        await ctxobj.send(content=title + f'{mention}' + mes, file=discord.File(Path(epath)))
                    else:
                        if oldmesobj:
                            await oldmesobj.edit(content=title + f'{mention}' + mes)
                        else:
                            self.ctx_objs[ctxid]['mesobj'] = await ctxobj.send(content=title + f'{mention}' + mes)
                        

                self.check_ctxobj_times()
                #time.sleep(0.1)
    def format_uts_mes(self, mes, authname):
        authname = authname + '_discord'
        if authname in mes:
            if mes.find(authname) == 0:
                newmes = '**' + authname + '** '
                mes = mes.replace(authname, '')
                newmes += mes
                return newmes
        return mes


    def check_ctxobj_times(self):
        current_time = time.time()
        if current_time - self.prev_checkctx_time > self.clear_ctx_wait:
            self.prev_checkctx_time = current_time
            rm = []
            for sdat in self.ctx_objs:
                dat = self.ctx_objs[sdat]
                stime = dat['time']
                if current_time - stime > self.max_ctx_time:
                    rm.append(sdat)
            for sdat in rm:
                self.ctx_objs.pop(sdat)

    def get_rand_quote(self, topic):
        while True:
            mes = self.humpty.rand_quote(topic)
            lmes = len(mes)
            if lmes < 2000 or not lmes:  
                return mes

    def get_uts_embed(self):
        embed = discord.Embed()
        embed.set_author(
                name='dtGames',
                url='https://twitter.com/_dtgames',
                icon_url= 'https://static.wixstatic.com/media/e7a94e_da51ae208c3e4dae954e4b524eacc162~mv2.png'
                )
        return embed

    def get_ctx_id(self, ctx, mesobj):
        ctxid = str(self.ctx_count)
        ctxdata = {
            'obj': ctx,
            'time': time.time(),
            'mesobj': mesobj,
            'channel': ctx.channel,
            'channel_name': ctx.channel.name,
            'auth_name': ctx.author.name.lower(),
            'auth_mention': ctx.author.mention,
            }
        self.ctx_objs[ctxid] = ctxdata
        self.ctx_count += 1
        
        return ctxid

    def get_shitpost(self):
        print('Getting shitpost')
        top = ''
        mem = ''
        
        while True:
            top = self.get_rand_topic().lower()
            mem = self.get_rand_quote(top)
            if len(mem):
                break
            time.sleep(0.1)
        print('Selected topic: ' + top)
        print('Shitpost: ' + mem)
        mem = mem.replace('twitchquotes:', '')
        return mem
    
    def run_bot(self):
        self.bot.run(self.authkey)
    
    def get_rand_topic(self):
        topics = self.humpty.topics
        roll = randint(0, len(topics) -1)
        topic = topics[roll]
        print('Topic is ' + topic)
        return topic
    
    def get_total_users(self, ctx):
        channel = ctx.channel.name
        count = len(ctx.guild.members)
        return count
           
            
    def get_random_meme(self):
        allmemes = os.listdir('./memes')
        roll = randint(0, len(allmemes))
        memepath = './memes/' + allmemes[roll]
        return memepath
            
        


a = dtBot('a')
