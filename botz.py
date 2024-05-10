# botz.py
import os
import discord
from dotenv import load_dotenv
from threading import Thread

from modules import parser

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ajuda_txt = '''
Boas! Bem-vindo à ajuda do botz - bot dos bubz!
1.pede !ajuda
2.faz uma !nota e diz quando queres ser lembrado. Exemplo:
    - "!nota \"cortar o cabelo\" 6a feira"
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
        datetime, nota, feedback_str = parser.parse_nota(message.content)

        await message.channel.send(feedback_str)
        
client.run(TOKEN)

# if __name__ == "__main__":
#     monitoring_thread = Thread(target=Scheduling.start_monitoring)
#     monitoring_thread.start()
#     monitoring_thread.join()