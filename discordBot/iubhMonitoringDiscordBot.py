import discord
from discord.ext import commands
import sys
import os
# appends the system path, to import the __init__ module from the monitor library
from monitor.__init__ import *
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'monitor'))

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)
client.remove_command("help")

# executes when bot connects successfully to the server
@client.event
async def on_ready():
    print(f'{client.user.name} successfully connect!\n')
    print("Connected to the following Guild/s:")
    for i in range(len(client.guilds)):
        print(str(client.guilds[i]) + "\n")
        i += 1

# welcome message everytime a new member joins the server
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Welcome {member.name} to the unofficial IU server for IT courses. \n" 
                                 f"Please introduce yourself at the channel '#vorstellungsrunde'"
                                 f"You can use this bot to select a role to show everyone what you are studying.\n\n"
                                 f"To set your role please type the correct command in our chat.\n"
                                 f"If your set it wrong, want change it or your role is not listed, please contact"
                                 f"one of the moderators.\n"
                                 f"Informatik : !informatik \nWirtschaftsinformatik : !wirtschaftsinformatik\n"
                                 f"Medieninformatik : !medieninformatik \nComputer Science : !computer_science\n"
                                 f"Robotik : !robotic \n Mit IT Bezug : !mITb \n\n"
                                 f"If you want to find out what else I can do, type !help in the chat!\n"
                                 f"Have fun and be nice to everyone. 😉")


# help command to show the user all available functions and information the bot has
@client.command()
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.set_author(name="Help")
    embed.add_field(name="Commands:", value="!status -> shows the availability of IU websites")
    await ctx.author.send(embed=embed)


# uses the read_json_status() method to get all the availability information from the monitor and shows them in the chat
@client.command()
async def status(ctx):
    answer_string = ""
    cur_status = read_json_data_bot()  # returns all necessary data for the user as a dictionary
    # creates an understandable message for the user with the information from the dictionary
    for i in range(len(cur_status)):
        if cur_status.get(i)[3] == -1:
            last_off_time = "-"  # will be writen to the user if no "last offline time" is known
        else:
            last_off_time = cur_status.get(i)[3]  # executes if a last offline time is known
        answer_string += f"**{cur_status.get(i)[0]}**: \n" \
                         f"\tStatus: {online_offline_unstable(cur_status.get(i)[1])} " \
                         f"| Latency: {cur_status.get(i)[2]}ms | " \
                         f"Last Offline-Time: {last_off_time}\n"
        i += 1
    # embeds the message for the user in a cooler look then a normal message
    embed = discord.Embed(colour=discord.Colour.dark_green())  # creates the embed and sets the border colour
    embed.set_author(name="Status")  # "title" of the message
    embed.add_field(name=f"Online: {online_offline_unstable('GREEN')} Offline: {online_offline_unstable('RED')} "
                         f"Unstable: "
                         f"{online_offline_unstable('YELLOW')}\n\n", value=answer_string)  # textfield with information
    await ctx.author.send(embed=embed)


# currently broken because of missing permission and i can't figure out what this missing permission is....
@client.command()
async def informatik(ctx):
    for i in range(len(ctx.author.guild.roles)):
        if ctx.author.guild.roles[i].name == "Informatiker":
            print(ctx.author.guild.roles[i])
    for role in range(len(ctx.author.roles)):
        if ctx.author.roles[role].name == "Informatiker":
            print("there is nothing to do")
            break
        elif role == len(ctx.author.roles) - 1:
            await ctx.author.add_roles(ctx.author.guild.roles[i])
            print("role will be set")


# runs the TOKEN of the chosen bot
client.run('ODEwOTIxOTY0MTAwMjU1NzY0.YCqr7g.tGKPsONMJ5Yqj_PdiG0mgaWHyq0')
