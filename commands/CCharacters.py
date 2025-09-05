import discord
from discord.ext import commands
from discord import app_commands
from UserData.UserData import UserData
from .helpers import isModerator


class CCharacters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="characters", description="Показать список ваших персонажей")
    @app_commands.describe(private_message="Только вы видите сообщение")
    async def characters(
        self, interaction: discord.Interaction, private_message: bool = True
    ):
        user = interaction.user
        userData = UserData(interaction.guild.id, user.id)
        characters = userData.characters
        charactersCount = len(characters)

        await interaction.response.send_message(
            f"У вас **{charactersCount}** персонажей:\n"
            + "\n".join(f"**{char}**" for char in characters),
            ephemeral=private_message,
        )

    @app_commands.command(name="characters_mod", description="Показать список персонажей пользователя")
    @app_commands.describe(
        user="Пользователь", private_message="Только вы видите сообщение"
    )
    @isModerator()
    async def characters_mod(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        private_message: bool = True,
    ):
        userData = UserData(interaction.guild.id, user.id)
        characters = userData.characters
        charactersCount = len(characters)

        await interaction.response.send_message(
            f"У {user.mention} **{charactersCount}** персонажей:\n"
            + "\n".join(f"**{char}**" for char in characters),
            ephemeral=private_message,
        )

    @app_commands.command(name="add_character", description="Добавить пользователю персонажа")
    @app_commands.describe(
        user="Пользователь",
        name="Имя персонажа",
        private_message="Только вы видите сообщение",
    )
    @isModerator()
    async def add_character(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        name: str,
        private_message: bool = True,
    ):
        userData = UserData(interaction.guild.id, user.id)
        characters = userData.characters
        characters.append(name)
        userData.characters = characters  # вызывается setter, сохраняет данные

        used = len(userData.characters)
        total = userData.characterSlots

        await interaction.response.send_message(
            f"Персонаж **{name}** добавлен для {user.mention}.\n"
            f"Теперь у {user.mention} занято **{used}** из **{total}** слотов."
        )


"""     @app_commands.command(name="characters_mod", description="Управление персонажами")
    @app_commands.describe(
        user="Пользователь",
        name="Имя персонажа",
        private_message="Только вы видите сообщение",
    )
    @isModerator()
    async def characters_mod(
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
        ) """
