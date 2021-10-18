import discord
from discord.ext.commands import command
from discord.ext import commands
import ast
import random
from num2words import num2words
import emoji
from googleapiclient.discovery import build

from bot import cur, conn, ordinaltg, youtube_api_key

class Dashboard(commands.Cog, name='Dashboard'):
    def __init__(self, bot):
        self.bot = bot
    #Primary Logic

    @property
    def random_color(self):
        return discord.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    @command()
    async def newdb(self, ctx):
        name = 'PLACEHOLERNAME1234567890123456789012345678901234567890'
        dashboard = {}


        if ctx.author.id == 893202343913467905:
            return
        
        await ctx.message.reply("Enter a name for your new dashboard")

        while len(name) > 32:
            reply = await self.bot.wait_for('message')

            if reply.author.id == self.bot.user.id:
                continue

            name = str(reply.content)

            if len(name) > 32:
                await reply.reply('Too long')
                continue

        await reply.reply('Now we will define playlists links / music links coupled with the theme name for {} dashboard'.format(name))
            
        finished = False
        count = 1


        while finished == False:
            await reply.reply('Define the name of your {} theme!, reply with "finished" if you do not want any more themes. (MAX THEMES = 9)'.format((ordinaltg(count))))

            themename = '12345678901234567890123456789012345678901234567890123456789012345678901234567890'

            while len(themename) > 32:

                reply = await self.bot.wait_for('message')

                if reply.author.id == self.bot.user.id:
                    continue

                if reply.content.lower() == 'finished':
                    finished = True
                    break
                
                themename = reply.content

                if len(themename) > 32:
                    await reply.reply('Too long!')
                    continue

                break

            if finished == True:
                break

            urls = []

            await reply.reply('Now send all the links or YouTube titles you want to associate with this theme. One per message. Type "Done" when finished.')

            Done = False
            
            while Done == False:
                reply = await self.bot.wait_for('message')

                if reply.author.id == self.bot.user.id:
                    continue

                if reply.content.lower() == 'finished':
                    finished = True
                    break

                if reply.content.lower() == 'done':
                    Done = True
                    break
                urls.append(str(reply.content))

            dashboard[themename] = urls
            count += 1

        id = str(ctx.author.id)
        id_name = str(id) + '_' + name
        dict = str(dashboard)

        cur.execute('''INSERT INTO dashboard(id_name, id, name, dict) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")''' % (id_name, id, name, dict))
        conn.commit()

    @command()
    async def dashboard(self, ctx, *, name:str):
        musicplayer = self.bot.get_cog('Music')

        #await musicplayer.disconnect_command(ctx)
        #await musicplayer.connect_command(ctx)

        id_name = str(ctx.author.id) + '_' + name


        query = 'SELECT dict FROM dashboard WHERE id_name = \"%s\"' % (id_name)
        cur.execute(query)
        dict = str(cur.fetchall())
        dict = ast.literal_eval(dict[3:-4])
        themes = dict.items()

        embed = discord.Embed(title=name, description="Your dashboard! Press the assigned button to switch themes!", color = (self.random_color))
        count = 1
        for theme in themes:
            theme_name = theme[0]
            theme_playlist = theme[-1]
            embed.add_field(name=theme_name, value=':' + str(num2words(count)) + ": " + str(theme_playlist), inline=False)
            count += 1
        embedded = await ctx.reply(embed=embed)

        emojis = ('\U00000031\U0000fe0f\U000020e3', '\U00000032\U0000fe0f\U000020e3', '\U00000033\U0000fe0f\U000020e3', '\U00000034\U0000fe0f\U000020e3', '\U00000035\U0000fe0f\U000020e3', '\U00000036\U0000fe0f\U000020e3', '\U00000037\U0000fe0f\U000020e3', '\U00000038\U0000fe0f\U000020e3', '\U00000039\U0000fe0f\U000020e3')
        for i in range(0, len(themes)):
            await embedded.add_reaction(emojis[i])
        
        def check(reaction, user):
            return user == ctx.message.author

        # dashboard loop

        bleh = True       

        while bleh:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if reaction != None:
                await musicplayer.stop_command(ctx)
                n = ( emoji.demojize(reaction.emoji) )[-2]
                n = int(n) - 1
                theme_to_play = ( list(themes)[n] )[-1]       
                for x in theme_to_play:
                    await musicplayer.play_command(ctx, query=x)
                await reaction.remove(user)               



def setup(bot):
    bot.add_cog(Dashboard(bot))
