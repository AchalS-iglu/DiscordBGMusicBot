import discord
from discord.ext import commands
import os
from  dotenv import load_dotenv
import youtube_dl
import sqlite3

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
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
} 
#-----------------------------------------------------------------------------------------------------------------

def endSong(guild, path):
    os.remove(path)

def ordinaltg(n):
  return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

#-----------------------------------------------------------------------------------------------------------------


load_dotenv()

token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print("Bot is live!")

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='To play song')
async def play(ctx, url):

    if not ctx.message.author.voice:
        await ctx.send('you are not connected to a voice channel')
        return

    else:
        channel = ctx.message.author.voice.channel

    voice_client = await channel.connect()

    guild = ctx.message.guild

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    await ctx.send(f'**Music: **{url}')
    









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
        await reply.reply('Define the name of your {} theme!, reply with "finished" if you do not want any more themes.'.format((ordinaltg(count))))

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

        await reply.reply('Now send all the links you want to associate with this theme. One per message. Type "Done" when finished.')

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
    pass


if __name__ == "__main__" :
    bot.run(token)