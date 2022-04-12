import discord
from discord.ext import commands

color = 0xffb7c5


class GenshinCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def craft(self, message, want='', green='0', blue='0', purple='0'):
        types = ['green', 'blue', 'purple', 'gold']
        if want in types:
            if want == 'gold':
                amount = ((int(blue) + int(green) / 3) / 3 + int(purple)) / 3
            elif want == 'purple':
                amount = (int(blue) + int(green) / 3) / 3 + int(purple)
            elif want == 'blue':
                amount = int(green) / 3 + int(blue)
            myEmbed = discord.Embed(
                title="",
                description="With your materials, you can make a total of " +
                str(int(amount)) + ' ' + str(want) + " materials",
                color=color)
            await message.channel.send(embed=myEmbed)
        else:
            await message.channel.send('Please enter a valid material type')


def setup(bot):
    bot.add_cog(GenshinCommands(bot))
