import discord
from discord.ext import commands
import os
from  dotenv import load_dotenv
import sqlite3
from num2words import num2words

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

def ordinaltg(n):
  return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

#-----------------------------------------------------------------------------------------------------------------

load_dotenv()

exts=['music', 'dashboard']

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


@bot.event
async def on_ready():
    print("Bot is live!")
        
for i in exts:
    bot.load_extension(i)

if __name__ == "__main__" :
    bot.run(os.getenv("DISCORD_TOKEN"))