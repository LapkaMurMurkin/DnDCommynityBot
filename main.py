import discord
from discord.ext import commands
from commands.commands import setupCommands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)

    async def setup_hook(self):
        # Подключаем команды
        await setupCommands(self)
        # Синхронизация команд
        synced = await self.tree.sync()
        print(f"✅ Синхронизировано {len(synced)} команд")


bot = MyBot()


@bot.event
async def on_ready():
    print(f"✅ {bot.user} запущен.")


bot.run(TOKEN)
