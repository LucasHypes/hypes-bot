import requests
from bs4 import BeautifulSoup
import asyncio
import discord

ultima_partida = None

def extrair_dados_da_partida(tag):
    url = f"https://brawlify.com/stats/battles/{tag.strip('#')}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[ERRO] Não foi possível acessar Brawlify para a tag {tag}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    tabela = soup.find("div", class_="table-responsive")
    if not tabela:
        print("[INFO] Nenhuma tabela de partidas encontrada.")
        return None

    linha = tabela.select_one("table tbody tr")
    if not linha:
        print("[INFO] Nenhuma partida encontrada na tabela.")
        return None

    colunas = linha.find_all("td")
    if len(colunas) < 5:
        print("[INFO] Colunas da partida incompletas.")
        return None

    tipo = colunas[2].text.strip().lower()
    if "friendly" not in tipo:
        print("[INFO] Última partida não é amistosa.")
        return None

    mapa = colunas[1].text.strip()
    resultado = colunas[4].text.strip()

    return {
        "mapa": mapa,
        "tipo": tipo,
        "resultado": resultado
    }

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
                    print("[INFO] Partida enviada com sucesso!")
                    break
        await asyncio.sleep(60)