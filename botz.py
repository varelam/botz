# botz.py
import os
import discord
from dotenv import load_dotenv
from threading import Thread

from modules import parser

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ajuda_txt = '''
Boas! Bem-vindo à ajuda do botz - bot dos bubz!
1. Na dúvida, pede uma !ajuda
2. Para já podes fazer uma !nota e dizer quando queres ser lembrado.
\t2.1.  Instruções: "!nota \"[mensagem com espaços]\" [dia da semana]"
\t2.2.  Exemplo: "!nota \"ir à cerâmica\" sábado"
\t2.3.  Exemplo: "Bro faz aí uma !nota \"cortar o cabelo\" 6a"
3. Podes listar os eventos todos com !lista
4. Podes apagar os eventos com !cancelar [número do evento]
'''

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!ajuda" in message.content:
        await message.channel.send(ajuda_txt)

    if "!nota" in message.content:
        feedback_str = parser.parse_nota(message.content)
        await message.channel.send(feedback_str)

    if "!lista" in message.content:
        feedback_str = parser.list_notas()
        await message.channel.send(feedback_str)

    if message.content.startswith("!cancelar"):
        feedback_str = parser.erase_nota(message.content)
        await message.channel.send(feedback_str)
        
client.run(TOKEN)