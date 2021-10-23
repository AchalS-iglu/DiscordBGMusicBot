import discord
from discord.ext.commands import command
from discord.ext import commands
import ast
import random
from num2words import num2words
import emoji

from bot import cur, conn, ordinaltg

class DashboardNotFound(commands.CommandError):
    pass


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

        embed1 = discord.Embed(title='Create a Dashboard!', description="Enter a name for your new dashboard", color = (self.random_color))
        embed1m = await ctx.message.reply(embed=embed1)

        while len(name) > 32:
            reply = await self.bot.wait_for('message')

            if reply.author.id == self.bot.user.id:
                continue

            name = str(reply.content)

            if len(name) > 32:
                await reply.reply('Too long')
                continue
        
        embed2 = discord.Embed(title='Create a Dashboard!', description='Now we will define playlists links / music links / names coupled with the theme name for {} dashboard. Spotify links also work but currently spotify links are extremely slow and albums outright do not work.'.format(name), color = self.random_color)
        embed2m = await reply.reply(embed=embed2)
            
        finished = False
        count = 1


        while finished == False and count <= 9:
            embed3 = discord.Embed(title='Create a Theme!', description='Define the name of your {} theme!, reply with "finished" if you do not want any more themes. (MAX THEMES = 9)'.format((ordinaltg(count))), color = self.random_color)
            embed3m = await reply.reply(embed=embed3)

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

            embed4 = discord.Embed(title='Define your Theme!', description='Now send all the links or YouTube titles you want to associate with this theme. One per message. Type "Done" when all the names have been entered..', color = self.random_color)
            embed4m = await reply.reply(embed=embed4)

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
        await embed1m.delete()
        await embed2m.delete()
        await embed3m.delete()
        await embed4m.delete()


    @command()
    async def dashboard(self, ctx, *, name:str):
        
        musiccog = self.bot.get_cog('Music')
        musicplayer = musiccog.get_player(ctx)

        id_name = str(ctx.author.id) + '_' + name


        query = 'SELECT dict FROM dashboard WHERE id_name = \"%s\"' % (id_name)
        cur.execute(query)
        dict = str(cur.fetchall())
        if len(dict) == 2:
            raise DashboardNotFound
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
        await embedded.add_reaction('\U0000274e')
        
        def check(reaction, user):
            return user == ctx.message.author

        # dashboard loop

        bleh = True       

        while bleh:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            reactionstr = ( emoji.demojize(reaction.emoji) )
            if 'keycap' in reactionstr:
                musicplayer.queue.empty()
                await musicplayer.stop()
                n = reactionstr[-2]
                n = int(n) - 1
                theme_to_play = ( list(themes)[n] )[-1]       
                for x in theme_to_play:
                    await musiccog.play_command(ctx, query=x)
                musicplayer.queue.shuffle()
                await reaction.remove(user)     
            else:
                musicplayer.queue.empty()
                await musicplayer.stop()
                await musicplayer.teardown()
                await embedded.delete()
                break          
    @dashboard.error
    async def dashboard_error(self,ctx,exc):
        if isinstance(exc, DashboardNotFound):
            await ctx.send('Dashboard not found')



def setup(bot):
    bot.add_cog(Dashboard(bot))
