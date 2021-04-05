import discord
from discord.ext import commands
import random 
import time
import requests
#
def rdj(num):
        with open("dadjokes.txt", encoding='utf8') as dadjokes:
            dadjoken = dadjokes.readlines()
        ran_djnum = random.randint(0,len(dadjoken)-1)
        def dj(num1):
            dadjoke = dadjoken[num1].replace("\n", "")
            return(dadjoke)
        return dj(ran_djnum)
class drequests(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
    @commands.command(name = 'dadjoke', help = 'Runs a nice dad joke :)')
    async def dad(self, ctx):
        await ctx.send(f'{str(rdj(1))}...')
    @commands.Cog.listener('on_message')
    async def ObamaChiro(self, message):
        if message.content.__contains__('obama') == True and message.channel.id == 792976211386957865:
            await message.add_reaction(self.bot.get_emoji(792612766267473930))
            obama = await message.channel.send('https://imgur.com/a/KyA2HyE')
            obunga = await message.channel.send('<a:loading:792614091189518366>OBAMA MENTION DETECTED. CONVERTING INTO: **OBUNGA** <a:loading:792614091189518366>')
            obama
            obunga
            time.sleep(3)
            await obama.edit(content = "https://imgur.com/a/KyA2HyE", delete_after = 1)
            await obunga.edit(content = "**OBUNGA** CONVERTING NEARLY FINISHED", delete_after = 1)
            time.sleep(2)
            await message.channel.send('https://blenderartists.org/uploads/default/original/4X/b/b/6/bb6046d1663c5df4f3eef70d874636e3f9712439.jpg')
            await message.channel.send('Obama has converted into obunga, F.')
        elif message.content.__contains__('chiro') == True:
            chiro_emoji = self.bot.get_emoji(792611989036990474)
            await message.add_reaction(chiro_emoji)
    @commands.command(name = 'funfact', help = 'Gets a random fun fact :)')
    async def funfact(self, ctx):
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        dict = response.json()
        if response.status_code == 200:
            await ctx.send(dict.get('text'))
        else:
            await ctx.send(f'Ran into an error unfortunately. The status code is **{response.status_code}**')
    @commands.command(name = 'cat', help = 'Returns a random image of a cat')
    async def cat(self,ctx):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        dict = response.json()
        if response.status_code == 200:
            await ctx.send(dict[0]['url'])
        else:
            await ctx.send(f'Ran into an error unfortunately. The status code is **{response.status_code}**')
    @commands.command(name = 'gender', help = 'Guesses the gender of a name you input')
    async def gender(self,ctx,name):
        response = requests.get(f"https://api.genderize.io/?name={name}")
        dict = response.json()
        if response.status_code == 200:
            if dict.get('gender') == 'null':
                await ctx.send("Sorry, the name you searched doesn\'t really have a gender")
            else:
                await ctx.send(f"```Name: {name} \nGender: {dict.get('gender')} \nProbability: {(dict.get('probability')*100)}%```")
        else:
            await ctx.send(f'Ran into an error unfortunately. The status code is **{response.status_code}**')
    @commands.command(name = 'advice', help = 'Gives you advice :)')
    async def advice(self,ctx):
        response = requests.get("https://api.adviceslip.com/advice")
        dict = response.json()
        slip = dict.get('slip')
        if response.status_code == 200:
            await ctx.send(slip.get('advice'))
        else:
            await ctx.send(f'Ran into an error unfortunately. The status code is **{response.status_code}**')
    @commands.command(name = 'bbsearch', help = 'Searches a breaking bad character')
    async def bbsearch(self,ctx,*,search):
        newsearch = search.replace(" ","+")
        response = requests.get(f"https://www.breakingbadapi.com/api/characters?name={newsearch}")
        if response.status_code == 200:
            dict = response.json()
            searchnum = 0
            for i in dict:
                searchnum += 1
            multires = ''
            multinum = 0
            if searchnum > 1:
                for i in dict:
                    if multinum > 0:
                        multires += ", "
                    multires += str(dict[int(multinum)]['name'])
                    multinum +=1
                await ctx.send(f"There were {searchnum} results for your query. Showing the first one. List of all results: \n `{multires}` ")
            if searchnum > 0:
                embed=discord.Embed(title = dict[0]['name'])
                embed.set_author(name = "Breaking Bad API")
                embed.set_thumbnail(url = dict[0]['img'])
                embed.add_field(name = "Birthday", value = dict[0]['birthday'],inline=False)
                text = ''
                newdict = dict[0]['occupation']
                for i in newdict:
                    text += str(f"\n{i}")
                embed.add_field(name = "Occupation", value = text,inline=False)
                embed.add_field(name = "Status", value = dict[0]['status'],inline=False)
                embed.add_field(name = 'Nickname', value = dict[0]['nickname'],inline=False)
                embed.add_field(name = 'Actor', value = dict[0]['portrayed'],inline=False)
                await ctx.send(embed=embed)
            elif searchnum == 0:
                await ctx.send(f":( No results for `{search}`")
        else:
            await ctx.send(f'Ran into an error unfortunately. The status code is **{response.status_code}**')

def setup(bot):
   bot.add_cog(drequests(bot))