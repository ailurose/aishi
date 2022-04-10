'''
import discord, tweepy
from discord.ext import commands
from discord.utils import get
from api import twt
from raid import raids, gbfroles

color = 0xffb7c5

class GranblueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def raid(self, message, user=''):
        if user == '':
            myEmbed = discord.Embed(
                title="",
                description=
                "No twitter username input. Please input twitter username",
                color=color)
            await message.channel.send(embed=myEmbed)
        elif message.author != self.bot.user:
            try:
                battleID, raidName, msg = twt('raid', user)
                checker = ':Battle ID\nI need backup!'
                if checker in msg:
                    raid = raids()
                    for r in raid:
                        for types in raid[r]:
                            if raidName in types:
                                try:
                                    ping = get(message.guild.roles, name=r)
                                    await message.channel.send(ping.mention)
                                except AttributeError:
                                    myEmbed = discord.Embed(title="",
                                                            description="",
                                                            color=color)
                    myEmbed = discord.Embed(title="",
                                            description=msg,
                                            color=color)
                else:
                    myEmbed = discord.Embed(
                        title="",
                        description='There are no recent raid msgs from ' +
                        user,
                        color=color)
                await message.channel.send(embed=myEmbed)
                await message.channel.send(battleID)
            except tweepy.TweepError:
                await message.channel.send(
                    "This is a private account. `~raid` only works on public twitters. Aishi apologizes for the inconvenience."
                )
            except ValueError:
                await message.channel.send(
                    "Aishi cannot find a raid message on this account. Please try again."
                )

    @commands.command(name='gbfroles')
    async def gbfRoles(self, message):
        myEmbed = discord.Embed(
            title='Granblue Roles',
            description=
            'Granblue roles have been created! Members can now join roles by using reacting to emojis \n',
            color=color)
        raid = raids()
        raidNames = list(raid)
        reactions = gbfroles()
        for index in range(len(raidNames)):
            reaction = reactions[index]
            types = raid[raidNames[index]]
            t_str = ''
            for t in types:
                t_str += t + '\n'
            myEmbed.add_field(name=reaction + ' ' + raidNames[index],
                              value=t_str)
        text = await message.send(embed=myEmbed)

        global reaction_message_id
        reaction_message_id = text.id

        for role in reactions:
            await text.add_reaction(emoji=role)
        await message.message.delete()

    @commands.Cog.listener('on_raw_reaction_add')
    async def add_role(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        if reaction_message_id != payload.message_id:
            return

        reactions = gbfroles()
        reaction = payload.emoji.name
        if reaction not in reactions:
            return

        role_names = list(raids())
        role_name = role_names[reactions.index(reaction)]
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name=role_name)
        await member.add_roles(role)

    @commands.Cog.listener('on_raw_reaction_remove')
    async def remove_role(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return

        if reaction_message_id != payload.message_id:
            return

        reactions = gbfroles()
        reaction = payload.emoji.name
        if reaction not in reactions:
            return

        role_names = list(raids())
        role_name = role_names[reactions.index(reaction)]
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name=role_name)
        await member.remove_roles(role)

def setup(bot):
    bot.add_cog(GranblueCommands(bot))
'''