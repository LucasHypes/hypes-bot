import requests
from bs4 import BeautifulSoup
import asyncio
import discord

ultima_partida = None

def extrair_dados_da_partida(tag):
    url = f"https://brawlify.com/stats/battles/{tag.strip('#')}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[ERRO] Não foi possível acessar Brawlify para o jogador {tag}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    partida = soup.find("div", class_="table-responsive")
    if not partida:
        print("[INFO] Nenhuma partida encontrada.")
        return None

    linhas = partida.select("table tbody tr")
    for linha in linhas:
        colunas = linha.find_all("td")
        if len(colunas) >= 5:
            tipo = colunas[2].text.strip().lower()
            if "friendly" in tipo:
                mapa = colunas[1].text.strip()
                resultado = colunas[4].text.strip()
                return {
                    "mapa": mapa,
                    "tipo": tipo,
                    "resultado": resultado
                }

    return None

async def monitorar_partidas(bot, canal_nome, tag_jogador):
    global ultima_partida
    await bot.wait_until_ready()

    while not bot.is_closed():
        print("[INFO] Verificando nova partida...")
        dados = extrair_dados_da_partida(tag_jogador)
        if dados and dados != ultima_partida:
            ultima_partida = dados
            msg = (
                f"📊 **Nova partida amistosa detectada!**\n"
                f"🗺️ Mapa: `{dados['mapa']}`\n"
                f"🎮 Tipo: `{dados['tipo']}`\n"
                f"🏆 Resultado: `{dados['resultado']}`"
            )
            for guild in bot.guilds:
                canal = discord.utils.get(guild.text_channels, name=canal_nome)
                if canal:
                    await canal.send(msg)
                    break
        await asyncio.sleep(60)