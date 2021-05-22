import discord
from discord.ext import commands
import sys
import os

# appends the system path, to import the __init__ module from the monitor library
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'monitor'))
from monitor.__init__ import *

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)
client.remove_command("help")


# executes when bot connects successfully to the server
@client.event
async def on_ready():
    print(f'{client.user.name} successfully connect!\n')
    print("Connected to the following Guild/s:")
    for i in range(len(client.guilds)):
        print(str(client.guilds[i]))
        i += 1
    print("\nReady to receive commands\n")


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


# finds index of role
def get_role_number(role, roles):
    for i in range(len(roles)):
        if roles[i].name == role:
            return i
    return -1


# makes sure if a user already has a specified role
def is_user_role(user, new_role):
    for role in range(len(user.roles)):
        if user.roles[role].name == new_role:
            return True
    return False


# use ctx.author and desired role name to set the users role
async def set_user_role(user, role):
    if is_user_role(user, role):
        print("User " + str(user) + " already has that role!")
        return
    role_number = get_role_number(role, user.guild.roles)
    if role_number != -1:
        print("Setting " + str(user) + " to role: " + role)
        await user.add_roles(user.guild.roles[role_number])
    else:
        print("Role not found: " + role)


# sets users role to informatik
@client.command()
async def informatik(ctx):
    await set_user_role(ctx.author, "Informatiker")


# runs the TOKEN of the chosen bot
client.run('ODEwOTIxOTY0MTAwMjU1NzY0.YCqr7g.tGKPsONMJ5Yqj_PdiG0mgaWHyq0')
