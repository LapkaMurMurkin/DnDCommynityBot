import discord
from discord.ext import commands
from discord import app_commands
from UserData.UserData import UserData
from .helpers import isModerator


class CPoints(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="points", description="Показать ваши очки сервера")
    @app_commands.describe(private_message="Только вы видите сообщение")
    async def points(
        self, interaction: discord.Interaction, private_message: bool = True
    ):
        user = interaction.user
        userData = UserData(interaction.guild.id, user.id)

        await interaction.response.send_message(
            f"У вас сейчас **{userData.serverPoints}** очков.",
            ephemeral=private_message,
        )

    @app_commands.command(name="points_mod", description="Управление очками сервера пользователя")
    @app_commands.describe(
        user="Пользователь",
        points="Количество очков (+/-)",
        private_message="Только вы видите сообщение",
    )
    @isModerator()
    async def points_mod(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        points: int = None,
        private_message: bool = True,
    ):
        userData = UserData(interaction.guild.id, user.id)

        # Если points не указан, просто показать очки
        if points is None:
            return await interaction.response.send_message(
                f"У {user.mention} сейчас **{userData.serverPoints}** очков.",
                ephemeral=private_message,
            )

        # Если points указан, изменяем очки
        userData.serverPoints += points
        sign = "добавлено" if points > 0 else "отнято"
        await interaction.response.send_message(
            f"У {user.mention} {sign} **{abs(points)}** очков.\n"
            f"Теперь у него {userData.serverPoints} очков.",
        )
