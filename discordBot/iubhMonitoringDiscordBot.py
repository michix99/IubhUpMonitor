import discord
from discord.ext import commands
import sys
import os
# appends the system path, to import the __init__ module from the monitor libary
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'monitor', 'monitor'))
from monitor.monitor.__init__ import *

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)


# executes when bot connected successfully to the server
@client.event
async def on_ready():
    print(f'{client.user.name} successfully connect!')
    status = read_json_status()
    print(status.get(1)[0])


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Welcome {member.name} to ...")


# runs the TOKEN of the choosen bot
client.run()
