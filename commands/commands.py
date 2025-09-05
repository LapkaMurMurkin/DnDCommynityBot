from discord.ext import commands
from .CPoints import CPoints
from .CRoll20 import CRoll20
from .CSlots import CSlots
from .CCharacters import CCharacters
from .CContent import CContent


async def setupCommands(bot: commands.Bot):
    await bot.add_cog(CPoints(bot))
    await bot.add_cog(CRoll20(bot))
    await bot.add_cog(CSlots(bot))
    await bot.add_cog(CCharacters(bot))
    await bot.add_cog(CContent(bot))
    bot.tree.add_command(CContent.CContentMod())
