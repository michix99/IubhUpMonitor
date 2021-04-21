import discord
from discord.ext import commands
import sys
import os
# appends the system path, to import the __init__ module from the monitor libary
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'monitor'))
from monitor.__init__ import *

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)
client.remove_command("help")


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
    await member.dm_channel.send(f"Welcome {member.name} to the unofficial IU server for computer scientiest and simulars. \n" 
                                 f"At first, please introduce yourself at the channel 'vorstellungsrunde' and set your role"
                                 f"based on the study you are doing at the IU. This will help other people to see at the first look"
                                 f"what kind of study your are practising.\n\n"
                                 f"To set your role please look at this list and type the correct command in our chat.\n"
                                 f"WARNING: You can set your role only one time. If your set it wrong, wanna change it or your"
                                 f"role isn't listed, then please contact an admin.\n"
                                 f"Informatik - !informatik \nWirtschaftsinformatik - !wirtschaftsinformatik\n"
                                 f"Medieninformatik - !medieninformatik \nComputer Science - !computer_science\n"
                                 f"Robotik - !robotic \n Mit IT Bezug - !mITb \n\n"
                                 f"For more instructions please fell free to ask the community or write !help in our chat"
                                 f"so you can see what kind of action I'm supporting.\n"
                                 f"Have fun and be nice to everyone. 😉")


# help command to show the user all available functions and informations the bot have
@client.command()
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.set_author(name="Help")
    embed.add_field(name="Commands:", value="!iu_websites_status -> shows the availability of the most used websites as an IU-student")
    await ctx.author.send(embed=embed)


# uses the read_json_status() method to get all the needed informations from the monitor and shows them in the chat
@client.command()
async def iu_websites_status(ctx):
    answer_string = ""
    status = read_json_data_bot()  # returns all necessary data for the user as a dictonary (function can be found in utils.py)
    # creates an understandable message for the user with the informations from the dictonary
    for i in range(len(status)):
        if status.get(i)[3] == -1:
            last_off_time = "-"  # will be writen to the user if no "last offline time" is known
        else:
            last_off_time = status.get(i)[3]  # executes if a last offline time is known
        answer_string += f"**{status.get(i)[0]}**: \n" \
                         f"\tStatus: {online_offline_unstable(status.get(i)[1])} | Latency: {status.get(i)[2]}ms | " \
                         f"Last Offline-Time: {last_off_time}\n"
        i += 1
    # embeds the message for the user in a cooler look then a normal message
    embed = discord.Embed(colour=discord.Colour.dark_green())  # creates the embed and sets the border colour
    embed.set_author(name="Status")  # "titel" of the message
    embed.add_field(name=f"Online: {online_offline_unstable('GREEN')} Offline: {online_offline_unstable('RED')} Unstable: "
                         f"{online_offline_unstable('YELLOW')}\n\n", value=answer_string)  # textfield with the inforamtion
    await ctx.author.send(embed=embed)


# runs the TOKEN of the choosen bot
client.run('ODEwOTIxOTY0MTAwMjU1NzY0.YCqr7g.tGKPsONMJ5Yqj_PdiG0mgaWHyq0')
