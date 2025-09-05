import discord
from discord.ext import commands
from discord import app_commands
from UserData.UserData import UserData
from .helpers import isModerator


class CContent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------------------------
    # /content — показать все ссылки пользователя
    # ---------------------------
    @app_commands.command(name="content", description="Доступный вам контент")
    @app_commands.describe(private_message="Только вы видите сообщение")
    async def content(
        self, interaction: discord.Interaction, private_message: bool = True
    ):
        user = interaction.user
        userData = UserData(interaction.guild.id, user.id)

        message = ""
        for key, links in userData.content.items():
            if links:  # если есть ссылки
                message += f"## {key.capitalize()}\n"
                for link in links:
                    message += f" - {link}\n"
                message += "\n"

        if not message:
            message = "У вас еще нет открытого контента."

        await interaction.response.send_message(message, ephemeral=private_message)

    # ---------------------------
    # /content_mod — группа подкоманд для модераторов
    # ---------------------------
    class CContentMod(app_commands.Group):
        def __init__(self):
            super().__init__(
                name="content_mod",
                description="Добавить пользователю контент",
            )

        async def add_link(
            self,
            interaction: discord.Interaction,
            user: discord.User,
            name: str,
            ref: str,
            content_type: str,
        ):
            userData = UserData(interaction.guild.id, user.id)
            server_content = userData.content

            link = f"[{name}](<{ref}>)"
            server_content[content_type].append(link)
            userData.content = server_content  # сохраняем

            await interaction.response.send_message(
                f"Добавлена ссылка на **{content_type.capitalize()}** для {user.mention}: {link}"
            )

        # Подкоманды
        @app_commands.command(name="race", description="Добавить ссылку на race")
        @app_commands.describe(user="Пользователь", name="Название", ref="Ссылка")
        @isModerator()
        async def race(
            self,
            interaction: discord.Interaction,
            user: discord.User,
            name: str,
            ref: str,
        ):
            await self.add_link(interaction, user, name, ref, "race")

        @app_commands.command(name="class", description="Добавить ссылку на class")
        @app_commands.describe(user="Пользователь", name="Название", ref="Ссылка")
        @isModerator()
        async def class_(
            self,
            interaction: discord.Interaction,
            user: discord.User,
            name: str,
            ref: str,
        ):
            await self.add_link(interaction, user, name, ref, "class")

        @app_commands.command(name="spell", description="Добавить ссылку на spell")
        @app_commands.describe(user="Пользователь", name="Название", ref="Ссылка")
        @isModerator()
        async def spell(
            self,
            interaction: discord.Interaction,
            user: discord.User,
            name: str,
            ref: str,
        ):
            await self.add_link(interaction, user, name, ref, "spell")
