import discord
import time
from discord.ext import commands
import random 
from discord.ext.commands import MemberConverter
from pretty_help import PrettyHelp
Alpha = False
owner_id = 1234 # replace with discord owner ID
intents = discord.Intents.default()
intents.members = True
bot = 1
TOKEN = 1
if Alpha == False:
    TOKEN = 'BOT TOKEN HERE'
    bot = commands.Bot(command_prefix='$', intents=intents)
elif Alpha == True:
    TOKEN = 'Alpha bot token' #ignore unless you want to have a seperate testing bot
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=PrettyHelp())
cogs = ["Utility", "Moderation", "Roblox", "drequests"]
@bot.event
async def on_ready():
    print('bot is running')
    if Alpha != True:
        channel = await bot.fetch_channel(792507115435458581) # deprecated
#        await channel.send("""""")
    elif Alpha == True:
        channel = await bot.fetch_channel(786340574915330078) # replace channel with your debugging channel, to let you know when the bot is running
        await channel.send("""@everyone bot is running""")
@bot.event
async def on_member_join(member):
    if Alpha == False:
        role = member.guild.get_role(786338736744038460) # replace with member role
        await member.add_roles(role)
        channel = member.guild.get_channel(792995673074958336) # join logs channel
        await channel.send(f'{member} has joined the discord! Welcome :)')
@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(792995673074958336) # leave logs, can be same as join logs
    message = await channel.send(f"lol noob {member} has left the discord. legit could care less.")
    message
    await message.add_reaction("😎")
if __name__ == "__main__": 
    for cog in cogs:
        bot.load_extension(cog)
print("hi user. the bot is starting up !!")
bot.run(TOKEN)
