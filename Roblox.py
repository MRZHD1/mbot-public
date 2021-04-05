import discord
from discord.ext import commands
import ro_py
from ro_py.client import Client
from ro_py.groups import Group
import requests
import json
import typing
#
rtoken = ".ROBLOXSECURITY TOKEN" #replace with token, including the DO NOT SHARE
groupid = 1234 #replace with group ID you want to demote/promote/shout in 
client = Client(token=rtoken)
cnv_id = 1234 #replace with conversation id
owner_id = 1234 # I think you know where this is going
class Roblox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.cooldown(1, 15, commands.cooldowns.BucketType.guild)
    @commands.command(name = 'rfind', help = 'Fetches a roblox user information')
    async def grab_info(self, ctx, arg):
        await ctx.send(f"Loading user {arg}...")
        try:
            user = await client.get_user_by_username(arg)
            await ctx.send("Found user.")
            rb_status = await user.get_status() or 'None.'
            rb_friend = await user.get_friends_count()
            rb_follower = await user.get_followers_count()
            await ctx.send(f"User: {arg} \nProfile Link: <https://www.roblox.com/users/{user.id}/profile> ``` Display Name: {user.display_name} \n Description: {user.description} \n Status: {rb_status} \n Friend count: {rb_friend} \n Follower count: {rb_follower}```  ")
            print(f'{arg} : {user.id}')
        except:
            await ctx.send(f'{arg} could not be found.')
    @commands.command(name = 'rsend')
    async def rsend(self, ctx, *, arg):
        if ctx.message.author.id == owner_id:
            conversation = await client.chat.get_conversation(cnv_id)
            await conversation.send_message(arg)
            await ctx.send(f'Sent the user with the message: {arg}')
        else:
            ctx.send('You aren\'t authorized to run this command')
    @commands.command(name = 'gshout')
    async def gshout(self, ctx, *, arg):
        if ctx.message.author.id == owner_id:
            group = await client.get_group(groupid) 
            await group.update_shout(arg)
            await ctx.send(f'Updated the group shout to {arg}')
        else:
            ctx.send('You aren\'t authorized to run this command')
    @commands.command(name = 'gpromote')
    async def gpromote(self, ctx, arg):
        if ctx.message.author.id == owner_id:
            try:
                group = await client.get_group(groupid)
                user = await client.get_user_by_username(arg)
                member1 = await group.get_member_by_id(user.id)
                await member1.change_rank(1)
                await ctx.send(f'User **{arg}** has been promoted.')
            except ro_py.utilities.errors.ApiError:
                await ctx.send('I don\'t have permission to perform this task.')
            #except ro_py.utilities.errors.NotFound:
            #    await ctx.send('This user was not found in the group.')
            # [deprecated]
            except AttributeError:
                await ctx.send(f'This raised an error, but it was ignored, as **{arg}** has been promoted.')
        else:
            ctx.send('You aren\'t authorized to run this command')
    @commands.command(name = 'gdemote')
    async def gdemote(self, ctx, arg):
        if ctx.message.author.id == owner_id:
            try:
                group = await client.get_group(groupid)
                user = await client.get_user_by_username(arg)
                member2 = await group.get_member_by_id(user.id)
                await member2.change_rank(-1)
                await ctx.send(f'User **{arg}** has been demoted.')
            except ro_py.utilities.errors.ApiError:
                await ctx.send('I don\'t have permission to perform this task.')
            #except ro_py.utilities.errors.NotFound:
            #   await ctx.send('This user was not found in the group.')
            except AttributeError:
                await ctx.send(f'This raised an error, but it was ignored, as **{arg}** has been demoted.')
        else:
            ctx.send('You aren\'t authorized to run this command')
    @commands.command(name = 'gjoin')
    async def gjoin(self, ctx):
        if ctx.message.author.id == owner_id:
            pass
        else:
            ctx.send('You aren\'t authorized to run this command')
    @commands.command(name = 'verify', help = "Binds your roblox account to your discord")
    async def verify(self, ctx, search : typing.Optional[discord.User]=None):
        if search != None:
            if ctx.message.author.id == owner_id:
                response = requests.get(f"https://verify.eryn.io/api/user/{search.id}")
                dict = response.json()
                if response.status_code == 200:
                    rUsername = dict.get('robloxUsername')
                    await ctx.send(f"The member you were searching for (**{search}**) has the ROBLOX username: {rUsername}")
                else:
                    await ctx.send("The user does not have a ROBLOX account linked with rover.")
            else:
                await ctx.send("You aren't authorized to search for other users. Try using `!verify` only, with no arguments.")
        elif search == None:
            response = requests.get(f"https://verify.eryn.io/api/user/{ctx.author.id}")
            dict = response.json()
            if response.status_code == 200:
                rUsername = dict.get('robloxUsername')
                newnick = f"{ctx.author.name} ({rUsername})"
                try:
                    await ctx.author.edit(nick = newnick, reason = "User verified")
                    await ctx.send(f"Found your ROBLOX account! Hello, **{newnick}**. I also changed your nickname, but you can change it back if you want.")
                except:
                    await ctx.send(f"I found your ROBLOX account, **{rUsername}**, but I was unable to change your nickname.")
            else:
                await ctx.send("You don't have a ROBLOX account attached to your discord. Verify here: <https://verify.eryn.io/> and try again.")
        else:
            await ctx.send("An unkown error occured. Please contact the owner.")
    @commands.command(name = 'rfilter', help = 'Puts your text through the genuine ROBLOX filter')
    async def filter(self, ctx, *, arg : str):
        message = await ctx.send("Attempting to send your message through the ROBLOX filter")
        message
        filteredmsg = await client.filter_text(arg)
        await message.edit("Your message, filtered: ", f"`{filteredmsg}`")
def setup(bot):
    bot.add_cog(Roblox(bot))
