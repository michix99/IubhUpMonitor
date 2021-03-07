import discord
from discord.ext import commands
import sys
sys.path.append('C:\\Users\\Kimana\\OneDrive - Linde Group\\Studien Projekt\\IubhUpMonitor\\monitor\\monitor')
from monitor.monitor.__init__ import *

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)


# executes when bot connected successfully to the server
@client.event
async def on_ready():
    print(f'{client.user.name} successfully connect!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Welcome {member.name} to ...")

# runs the TOKEN of the choosen bot
client.run()
