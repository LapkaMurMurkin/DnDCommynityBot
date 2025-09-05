import discord
from discord.ext import commands
from discord import app_commands
from UserData.UserData import UserData
from .helpers import isModerator


class CRoll20(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="roll20", description="Ваш никнейм на Roll20")
    @app_commands.describe(private_message="Только вы видите сообщение")
    async def roll20(
        self, interaction: discord.Interaction, private_message: bool = True
    ):
        user = interaction.user
        userData = UserData(interaction.guild.id, user.id)

        await interaction.response.send_message(
            f"Ваш никнейм на Roll20: **{userData.roll20Name}**",
            ephemeral=private_message,
        )

    @app_commands.command(
        name="roll20_mod", description="Управление никнеймом пользователся на Roll20"
    )
    @app_commands.describe(
        user="Пользователь",
        roll20name="Никнейм для установки",
        private_message="Только вы видите сообщение",
    )
    @isModerator()
    async def roll20_mod(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        roll20name: str = None,
        private_message: bool = True,
    ):
        userData = UserData(interaction.guild.id, user.id)

        if roll20name is None:
            return await interaction.response.send_message(
                f"Текущий никнейм пользователя {user.mention}: **{userData.roll20Name}**",
                ephemeral=private_message,
            )

        userData.roll20Name = roll20name
        await interaction.response.send_message(
            f"Для {user.mention} установлен никнейм: **{roll20name}**",
        )
