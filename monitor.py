import discord
import aiohttp
import asyncio
from config import API_URL

ultima_partida_id = None

async def monitorar_partidas(bot, canal_nome: str, tag_jogador: str):
    global ultima_partida_id

    await bot.wait_until_ready()
    canal = discord.utils.get(bot.get_all_channels(), name=canal_nome)

    if not canal:
        print(f"❌ Canal '{canal_nome}' não encontrado.")
        return

    while not bot.is_closed():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL) as resp:
                    if resp.status != 200:
                        print(f"❌ Erro na API: {resp.status}")
                        await asyncio.sleep(30)
                        continue
                    
                    dados = await resp.json()

            if "erro" in dados:
                print("ℹ️ Nenhuma partida encontrada.")
                await asyncio.sleep(30)
                continue

            partida_id_atual = f"{dados['modo']}-{dados['mapa']}-{dados['resultado']}"

            if partida_id_atual != ultima_partida_id:
                ultima_partida_id = partida_id_atual
                mensagem = (
                    f"📊 Nova partida amistosa detectada!\n"
                    f"🗺️ Mapa: {dados['mapa']}\n"
                    f"🏆 Resultado: {dados['resultado']}\n"
                    f"🎮 Modo: {dados['modo']}"
                )
                await canal.send(mensagem)
            else:
                print("🔁 Nenhuma nova partida.")

        except Exception as e:
            print(f"⚠️ Erro durante monitoramento: {e}")

        await asyncio.sleep(30)