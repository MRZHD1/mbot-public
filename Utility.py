import discord
from discord.ext import commands
import time
from discord.ext.commands import MemberConverter
from googlesearch import search
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = 'say', help = 'Copies your text noob !1')
    async def say(self,ctx, *, arg):
        await ctx.message.delete()
        embed=discord.Embed(title=f"{arg}")
        embed.set_footer(text=f"invoked by {ctx.message.author}")
        embed.set_author(name="MitchBot", icon_url="https://cdn.discordapp.com/avatars/792502421112619028/460fbaf0d54bdf747ec99690a38f20ab.png?size=256")
        await ctx.send(embed=embed)
    @commands.command(name='users', help = 'Fetches the guild\'s user count.')
    async def users(self, ctx):
        guild = self.bot.get_guild(786338033342873610)
        await ctx.send(f'`There are {guild.member_count} members in {guild.name}`')
    @commands.command(name = 'presence', help = 'changes the bot\'s status!1 1')
    async def presence(self, ctx,*, arg):
        if ctx.message.author.id == 617151057633607718:
            await self.bot.change_presence(activity = discord.Game(str(arg)))
            await ctx.send(f'Changed the bot\'s status to {str(arg)}')
            await ctx.message.delete()
        else:
            await ctx.send('You are not authorized to run this command')
    @commands.command(name = 'dm', help = 'just dms the person lol')
    async def dm(self, ctx, user : discord.User, *, cmessage):
        embed=discord.Embed()
        embed.add_field(name="New Message!", value= f" --", inline=False)
        embed.add_field(name = f'`{cmessage}`', value=f'‎‎‎')
        embed.set_footer(text=f"Sent by {ctx.author}", icon_url = f'{ctx.author.avatar_url}')
        await user.send(embed=embed)
        await ctx.send(f'The message was sent to {user}!')
#   await user.send(f"||Sent by {ctx.author.display_name} via VX Helper.||")
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.guild)
    @commands.command(name = 'google', help = 'Googles your query :)')
    async def google(self,ctx,*,squery):
        sembed=discord.Embed()
        sembed.set_author(name = "Searching for your query....")
        sembed.set_thumbnail(url = "https://res-3.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco/fa8nmvofinznny6rkwvf")  
        message = await ctx.send(embed=sembed)
        message
        embed=discord.Embed()
        embed.set_author(name = "Google search")
        embed.set_thumbnail(url = "https://res-3.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco/fa8nmvofinznny6rkwvf")  
        query = squery
        snum = 0
        for i in search(query, tld = "com", num=5, stop=5, pause =2):
            snum+=1
            embed.add_field(name = f"Result #{snum}:", value = f"[{i}]({i})",inline=False)
            embed.set_footer(text = f"Search was requested by {ctx.author}")
        await message.edit(embed=embed)
    @commands.command(name = 'ping', help = 'Sends the bot ping') # this command was out-sourced.
    async def ping(self, ctx):
        if round(self.bot.latency * 1000) <= 50:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0x44ff44)
        elif round(self.bot.latency * 1000) <= 100:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0xffd000)
        elif round(self.bot.latency * 1000) <= 200:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0xff6600)
        else:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0x990000)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Utility(bot))
