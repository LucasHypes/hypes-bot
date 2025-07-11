import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Estou online!")

keep_alive()
bot.run(DISCORD_TOKEN)
