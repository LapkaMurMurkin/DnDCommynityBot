import discord
from discord.ext import commands
import json
import os

TOKEN = ""
DATA_FILE = "data.json"

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)


# ===== События =====
@bot.event
async def on_ready():
    print(f"✅ {bot.user} запущен.")

# ===== Тест =====
@bot.command()
async def hello(ctx):
    await ctx.reply("hello")
    await ctx.send("hello2")


# ===== Команды =====
@bot.command()
async def addServerPoints(ctx, member: discord.Member, amount: int):
    """Добавить поинты пользователю"""
    add_points(ctx.guild.id, member.id, amount)
    await ctx.send(
        f"✅ {member.mention} получил **{amount}** очков. Теперь у него {get_points(ctx.guild.id, member.id)} очков."
    )


@bot.command()
async def subtractServerPoints(ctx, member: discord.Member, amount: int):
    """Отнять поинты у пользователя"""
    add_points(ctx.guild.id, member.id, -amount)
    await ctx.send(
        f"❌ У {member.mention} отнято **{amount}** очков. Теперь у него {get_points(ctx.guild.id, member.id)} очков."
    )


@bot.command()
async def showServerPoints(ctx, member: discord.Member):
    """Показать очки пользователя"""
    points = get_points(ctx.guild.id, member.id)
    await ctx.send(f"📊 У {member.mention} сейчас **{points}** очков.")

    # ===== Работа с данными =====


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_points(guild_id, user_id, points):
    data = load_data()
    guild_id = str(guild_id)
    user_id = str(user_id)

    if guild_id not in data:
        data[guild_id] = {}
    data[guild_id][user_id] = data[guild_id].get(user_id, 0) + points
    save_data(data)


def get_points(guild_id, user_id):
    data = load_data()
    return data.get(str(guild_id), {}).get(str(user_id), 0)


bot.run(TOKEN)
