import discord
from discord.ext import commands
import os
from  dotenv import load_dotenv
import youtube_dl
import sqlite3
import ast
import random
from num2words import num2words
import emoji
from music import MusicPlayer

conn = sqlite3.connect('test.db')
conn.commit()

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS "dashboard" (
	"id_name" VARCHAR(50) NOT NULL DEFAULT NULL,
	"id" INTEGER(18) NULL,
	"name" VARCHAR(32) NULL DEFAULT NULL,
	"dict" TEXT NULL DEFAULT NULL,
	PRIMARY KEY ("id_name")
);''')

conn.commit()
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------

def endSong(guild, path):
    os.remove(path)

def ordinaltg(n):
  return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

#-----------------------------------------------------------------------------------------------------------------

load_dotenv()

exts=['music']

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


@bot.event
async def on_ready():
    print("Bot is live!")

@bot.command(name='newdb', help='Create a new dashboard')
async def newdb(ctx):
    name = 'PLACEHOLERNAME1234567890123456789012345678901234567890'
    dashboard = {}


    if ctx.author.id == 893202343913467905:
        return
    
    await ctx.message.reply("Enter a name for your new dashboard")

    while len(name) > 32:
        reply = await bot.wait_for('message')

        if reply.author.id == bot.user.id:
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

            reply = await bot.wait_for('message')

            if reply.author.id == bot.user.id:
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
            reply = await bot.wait_for('message')

            if reply.author.id == bot.user.id:
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

@bot.command(name='dashboard', help='Open up a dashboard')
async def dashboard(ctx, *, name:str):

    id_name = str(ctx.author.id) + '_' + name


    query = 'SELECT dict FROM dashboard WHERE id_name = \"%s\"' % (id_name)
    cur.execute(query)
    dict = str(cur.fetchall())
    dict = ast.literal_eval(dict[3:-4])
    themes = dict.items()

    embed = discord.Embed(title=name, description="Your dashboard! Press the assigned button to switch themes!", color = (
        discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))

    ))
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

    something = True

    while something:        
        reaction, user = await bot.wait_for('reaction_add', check=check)
        n = ( emoji.demojize(reaction.emoji) )[-2]
        n = int(n)
        print(list(themes))
        theme_to_play = list(themes)[n]
        theme_to_play = theme_to_play
        
        




for i in exts:
    bot.load_extension(i)


if __name__ == "__main__" :
    bot.run(os.getenv("DISCORD_TOKEN"))