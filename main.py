import discord
from discord.ext import commands
from config import DISCORD_TOKEN, API_URL
from keep_alive import keep_alive
from monitor import monitorar_partidas

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user.name}')
    bot.loop.create_task(monitorar_partidas(bot, canal_nome="resultados", tag_jogador="#8VPG0PCPJ"))

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Estou online!")

keep_alive()
bot.run(DISCORD_TOKEN)