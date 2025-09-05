import discord
from discord import app_commands

ERROR_MESSAGE = "❌Сосал❌"

"""
async def isModerator(interaction: discord.Interaction) -> bool:
    
    Проверяет, есть ли у пользователя права модератора.
    Если прав нет — отправляет сообщение и возвращает False.
    
    perms = interaction.user.guild_permissions
    if perms.administrator:
        return True
    # Сообщение выводится только автору команды
    await interaction.response.send_message(ERROR_MESSAGE, ephemeral=True)
    return False
"""


def isModerator():
    """Декоратор для проверки прав модератора в slash-командах"""

    async def predicate(interaction: discord.Interaction) -> bool:
        perms = interaction.user.guild_permissions
        if perms.administrator:
            return True
        await interaction.response.send_message(ERROR_MESSAGE, ephemeral=True)
        return False

    return app_commands.check(predicate)
