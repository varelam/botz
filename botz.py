# botz.py
import os
import discord
from discord.ext import commands, tasks
import datetime
from dotenv import load_dotenv

from modules import parser
from modules import scheduling

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CAMINHA_ID')

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

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.my_background_task.start()

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if "!ajuda" in message.content:
            print("ajuda")
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

    @tasks.loop(seconds=60)
    async def my_background_task(self):
        now = datetime.datetime.now()
        if now.hour == 8 and now.minute == 30:
            message = scheduling.get_night_message()
            channel = self.get_channel(int(CHANNEL_ID))
            await channel.send(message)
        if now.hour == 7 and now.minute == 30:
            message = scheduling.get_morning_message()
            channel = self.get_channel(int(CHANNEL_ID))
            await channel.send(message)
        if now.hour == 0 and now.minute == 30:
            erase_log = scheduling.cleanup_events()

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(TOKEN)