import discord
from discord.ext import commands
from discord import app_commands
from UserData.UserData import UserData
from .helpers import isModerator


class CSlots(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="slots", description="Ваши слоты персонажей")
    @app_commands.describe(private_message="Только вы видите сообщение")
    async def slots(
        self, interaction: discord.Interaction, private_message: bool = True
    ):
        user = interaction.user
        userData = UserData(interaction.guild.id, user.id)
        used = len(userData.characters)
        total = userData.characterSlots

        await interaction.response.send_message(
            f"У вас занято **{used}** из **{total}** слотов.",
            ephemeral=True,
        )

    @app_commands.command(name="slots_mod", description="Управление слотами персонажей полоьзователя")
    @app_commands.describe(
        user="Пользователь",
        slots="Количество слотов (+/-)",
        private_message="Только вы видите сообщение",
    )
    @isModerator()
    async def slots_mod(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        slots: int = None,
        private_message: bool = True,
    ):
        userData = UserData(interaction.guild.id, user.id)
        used = len(userData.characters)
        total = userData.characterSlots

        # Если slots не указан, просто показать количество слотов
        if slots is None:
            return await interaction.response.send_message(
                f"У {user.mention} занято **{used}** из **{total}** слотов.",
                ephemeral=private_message,
            )

        userData.characterSlots += slots
        sign = "добавлено" if slots > 0 else "отнято"
        await interaction.response.send_message(
            f"У {user.mention} {sign} **{abs(slots)}** слотов.\n"
            f"Теперь у него **{userData.characterSlots}** слотов.\n"
            f"Занято **{used}** из **{userData.characterSlots}** слотов.",
        )
