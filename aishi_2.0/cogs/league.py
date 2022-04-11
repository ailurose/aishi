import discord
from discord.ext import commands
from api import mmr, riot

color = 0xffb7c5
regions = ['na', 'euw', 'eune']


class LeagueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ammr(self, message, user='', region='na'):
        if user == '':
            myEmbed = discord.Embed(
                title="",
                description="No summoner input. Please input summoner name",
                color=color)
            await message.channel.send(embed=myEmbed)
        elif message.author.id == '131908538938163200' and user.lower(
        ) == 'glancelot':
            myEmbed = discord.Embed(title="",
                                    description=user + "'s mmr is: 42069",
                                    color=color)
            print('fren prank working')
            await message.channel.send(embed=myEmbed)
        elif (message.author != self.bot.user):
            if region in regions:
                aram = mmr(user.lower(), 'ARAM', region)
                if aram == 'error':
                    myEmbed = discord.Embed(
                        title="",
                        description="There is no ARAM data on this user",
                        color=color)
                    await message.channel.send(embed=myEmbed)
                else:
                    myEmbed = discord.Embed(title="",
                                            description=user + "'s mmr is: " +
                                            str(aram),
                                            color=color)
                    await message.channel.send(embed=myEmbed)
            else:
                myEmbed = discord.Embed(
                    title="",
                    description=
                    "Invalid region. Please input one of the following regions when calling the command: \n\t`na = north america`\n\t`euw = EU West`\n\t`eune = EU Nordic & East`",
                    color=color)
                await message.channel.send(embed=myEmbed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def aram(self, message, user, region='na'):
        teams = riot(user.lower(), 'ARAM', region)
        if teams == 'error':
            myEmbed = discord.Embed(
                title="",
                description="There are no current ARAM games with " + user,
                color=color)
        elif teams == 'unableToRetrieve':
            myEmbed = discord.Embed(
                title="",
                description=
                'ARAM data is unable to be retrieved at this time... please try again later',
                color=color)
        elif teams != 'error' and teams != 'unableToRetrieve':
            yourTeam = ''
            enemyTeam = ''
            teamsList = ['team1', 'team2']
            for team in teamsList:
                for players in teams[team]:
                    mmrNum = str(players[1])
                    if mmrNum == 'error':
                        mmrNum = 'N/A'
                    if team == teams['playerTeam']:
                        yourTeam = yourTeam + '*' + players[
                            0] + '*  :  ' + '\t\t\t' + str(players[1]) + '\n'
                    else:
                        enemyTeam = enemyTeam + '*' + players[
                            0] + '*  :  ' + '\t\t\t' + str(players[1]) + '\n'
            myEmbed = discord.Embed(title="ARAM mmr",
                                    description="",
                                    color=color)
            myEmbed.add_field(name="Your Team", value=yourTeam)
            myEmbed.add_field(name="Enemy Team", value=enemyTeam, inline=False)
        await message.channel.send(embed=myEmbed)

def setup(bot):
    bot.add_cog(LeagueCommands(bot))
