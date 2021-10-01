import discord
from discord.ext import commands
import os
from  dotenv import load_dotenv
import youtube_dl
import asyncio
import sqlite3
import csv

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


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data    
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:   
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

#-----------------------------------------------------------------------------------------------------------------

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
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))

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

    await reply.reply('Now we will define playlists links / music links / music name coupled with the theme name for {} dashboard'.format(name))
        
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