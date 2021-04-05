import discord
from discord.ext import commands
import datetime
import pymongo
from pymongo import MongoClient 
from discord.ext.commands import MemberConverter
import typing
import dns
import asyncio
import time
timeout = time.time() + 30
owner_id = 1234 # replace with your ID
server_id = 1234 # replace with your server ID
try: 
    conn = pymongo.MongoClient("mongodb+srv://link123") # replace with a pymongo access link. Easy to set up and free.
    print("Connected successfully to the Mongo DataBase") 
except:   
    print("Could not connect to MongoDB") # Your bot WILL stop if it can't connect to the database
else:
    db = conn.Mitchbot
    class Moderation(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
        @commands.command(name = 'warn', help = 'dont get one of these')
        async def warn(self, ctx, wuser : discord.User,*, arg):
            if ctx.message.author.id == owner_id:
                collection = db.warnings
                warn_rec = { 
                "user":f"{str(wuser.id)}", 
                "warner":f'{ctx.message.author.id}',
                "reason":f'{arg}', 
                "date/time":f"{datetime.datetime.today()}"
                }
                print(f'Warning added with {warn_rec} as the data.')
                inserted_record = collection.insert_one(warn_rec) 
                print("Data inserted with record id",inserted_record)
                cursor = collection.find()
                for inserted_record in cursor:
                    print(inserted_record) 
                await ctx.send(f'{wuser.mention} has been warned by {ctx.message.author.mention} for **{str(arg)}**')
        @commands.command(name = 'warnings', help = 'Displays your warnings.')
        @commands.cooldown(1, 2, commands.cooldowns.BucketType.guild)
        async def warnings(self, ctx, arg: typing.Optional[discord.User] = 'MitchBot#8768'): #can really put any user you want as default
            if arg == 'MitchBot#8768':
                wcount = 0
                mcount = 0
                collection = db.warnings
                myquery = {"user": f"{ctx.message.author.id}"}
                findings = collection.find(myquery)
                findings2 = collection.find(myquery)
                embed = {}
                for y in findings2:
                    mcount+=1
                for x in findings:
                    wcount += 1
                    dict = x
                    embed[wcount]=discord.Embed()
                    embed[wcount].set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                    embed[wcount].add_field(name="Date/Time", value= f"{dict.get('date/time')}", inline=False)
                    embed[wcount].add_field(name="Reason: ", value= f"{dict.get('reason')}", inline=False)
                    embed[wcount].add_field(name="Warner:", value= f"<@{dict.get('warner')}>", inline=False)
                    embed[wcount].set_footer(text=f"Warning {wcount}/{mcount}")
                if wcount == 0:
                    await ctx.send("You don't have any warnings, silly.")
                else:
                    message = await ctx.send("",embed=embed[1])
                    message
                    await message.add_reaction('◀️')
                    await message.add_reaction('▶️')
                    count = 1
                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ["◀️", "▶️"]
                    while True:
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
                            print(reaction, user)
                            if str(reaction.emoji) == "▶️" and count < wcount: # if its less than max 
                                count += 1
                                await message.remove_reaction('▶️',ctx.message.author)
                                await message.edit(embed=embed[count])
                            elif str(reaction.emoji) == "▶️" and count == wcount: # if its at max
                                await message.remove_reaction('▶️',ctx.message.author)
                            elif str(reaction.emoji) == "◀️" and count == 1: # if its at min 
                                await message.remove_reaction('◀️',ctx.message.author)
                            elif str(reaction.emoji) == "◀️" and count > 1: # if its greater than min
                                count -= 1
                                await message.remove_reaction('◀️',ctx.message.author)
                                await message.edit(embed=embed[count])
                        except asyncio.TimeoutError:
                            await message.clear_reactions()
                            break
            elif ctx.message.author.id == owner_id:
                abc = 1
                # [WIP]
            else:
                await ctx.send("You don't have permission to view other user's warnings.")
        @commands.command(name = 'kick', help = 'uh.... it kicks.')
        async def kick(self, ctx, duser : discord.User):
                if ctx.message.author.id == owner_id:
                    guild = self.bot.get_guild(server_id)
                    await guild.kick(duser)
                    kicker = ctx.message.author
                    await ctx.send (f'{duser} has been kicked by {kicker.mention}')
                else:
                    await ctx.send(f'lol nice try {ctx.message.author.mention}')
        @commands.command(name = 'ban', help = 'this time it bans lol')
        async def ban(self, ctx, d_id):
            if ctx.message.author.id == owner_id:
                guild = self.bot.get_guild(server_id)
                await guild.ban(discord.Object(id=d_id))
                banner = ctx.message.author
                await ctx.send (f'haha <@{d_id}> got banned by {banner.mention}')
                await ctx.message.delete()
            else:
                await ctx.send(f'um who do u think u are. i aint banning {d_id} (real homie)')
        @commands.command(name = 'unban', help = 'only noobs use this')
        async def unban(self, ctx, ud_id):
            if ctx.message.author.id == owner_id:
                guild = self.bot.get_guild(server_id)
                await guild.unban(discord.Object(id=ud_id))
                unbanner = ctx.message.author
                await ctx.send (f'<@{ud_id}> literally just got unbanned by {unbanner.mention}. smh imagine sucking up to <@{ud_id}>. Loser.')
            else:
                await ctx.send(f'lol nice try {ctx.message.author.mention}')
    def setup(bot):
        bot.add_cog(Moderation(bot))
