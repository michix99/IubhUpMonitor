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
    print(f'{client.user.name} successfully connect!\n')
    print("Connected to the following Guild/s:")
    for i in range(len(client.guilds)):
        print(str(client.guilds[i]) + "\n")
        i += 1


# generated message everytime when a new member joins the server
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Welcome {member.name} to ...")


# uses the read_json_status() method to get all the needed informations from the monitor and shows them in the chat
@client.command()
async def website_status(ctx):
    answer_string = ""
    status = read_json_status()  # returns all necessary data for the user as a dictonary
    # creates an understandable message for the user with the informations from the dictonary
    for i in range(len(status)):
        answer_string += f"**{status.get(i)[0]}**: \n" \
                         f"\tStatus: {online_offline_unstable(status.get(i)[1])} | Latency: {status.get(i)[2]}\n"
        i += 1
    # embeds the message for the user in a cooler look then a normal message
    embed = discord.Embed(colour=discord.Colour.dark_green())  # creates the embed and sets the border colour
    embed.set_author(name="Status")  # "titel" of the message
    embed.add_field(name=f"Online: {online_offline_unstable('GREEN')} Offline: {online_offline_unstable('RED')} Unstable: "
                         f"{online_offline_unstable('YELLOW')}\n\n", value=answer_string)  # textfield with the inforamtion
    await ctx.author.send(embed=embed)


# delete the last messages
@client.command()
async def clear(ctx):
    await ctx.channel.purge()

# runs the TOKEN of the choosen bot
client.run('ODEwOTIxOTY0MTAwMjU1NzY0.YCqr7g.tGKPsONMJ5Yqj_PdiG0mgaWHyq0')
