import requests
from bs4 import BeautifulSoup
import asyncio

ultima_partida = None

def extrair_dados_da_partida(tag):
    url = f"https://brawlify.com/player/{tag.strip('#')}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[ERRO] Não foi possível acessar Brawlify para o jogador {tag}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    partidas = soup.find_all("div", class_="match-box")

    for partida in partidas:
        tipo = partida.find("div", class_="badge-mode").text.strip().lower()
        if "friendly" in tipo:
            mapa = partida.find("div", class_="mode-name").text.strip()
            resultado = partida.find("div", class_="match-result")
            resultado_texto = resultado.text.strip() if resultado else "Resultado desconhecido"
            return {
                "mapa": mapa,
                "tipo": tipo,
                "resultado": resultado_texto
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
                f"📊 **Nova partida amistosa jogada!**\n"
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