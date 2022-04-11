'''
This is all of the extra code that we have that does not have a particular category to them.
'''

import asyncio, discord, random, requests
from discord.ext import commands
from io import BytesIO
from petpetgif import petpet as petpetgif
from api import data

color = 0xffb7c5


class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ### feedback command for any users of aishi to input their feedback about the bot
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feedback(self, ctx):
        myEmbed = discord.Embed(
            title="Aishi Feedback",
            description=
            "If you wish to provide feedback on Aishi as a bot, please type `yes`\nOtherwise, please type `no` or `exit` to exit this menu.",
            color=color)
        await ctx.channel.send(embed=myEmbed)
        member = ctx.guild.get_member(ctx.author.id)
        memberid = ctx.author.id

        def check(m):
            return (m.content.lower() == 'yes' or m.content.lower() == 'no' or
                    m.content.lower() == 'exit') and m.author.id == member.id

        def check2(m):
            return m.author.id == memberid

        try:
            msg = await self.bot.wait_for("message", timeout=10, check=check)
        except asyncio.TimeoutError:
            await ctx.channel.send(
                "Aishi Feedback menu has timed out due to inactivity")
        else:
            if msg.content.lower() == 'yes':
                await ctx.channel.send(
                    "Please type and send your feedback regarding Aishi bot")
                try:
                    msg = await self.bot.wait_for("message", check=check2)
                    info = data('feedback', 'create', memberid, msg.content)
                    if info == 'error':
                        await ctx.channel.send(
                            "I'm sorry... your feedback wasn't recorded due to an error. Please try again later as Aishi appreciates your feedback."
                        )
                    elif info == 'timeout':
                        await ctx.channel.send(
                            "Please wait before sending another feedback on Aishi. Aishi appreciates your enthusiasm to send feedback on Aishi!"
                        )
                    else:
                        await ctx.channel.send(
                            "Thank you very much for your feedback! It is appreciated!"
                        )
                except asyncio.TimeoutError:
                    await ctx.channel.send(
                        "Aishi Feedback menu has timed out due to inactivity")
            elif msg.content.lower() == 'exit' or msg.content.lower() == 'no':
                return
            await msg.delete()

    ### coin flip command: flips a coin and returns heads or tails
    @commands.command()
    async def flip(self, message):
        coin = ['heads', 'tails']
        myEmbed = discord.Embed(title="",
                                description="You got " + random.choice(coin),
                                color=color)
        await message.channel.send(embed=myEmbed)

    ### github command: provides the github link of the bot
    @commands.command()
    async def github(self, message):
        githublink = 'https://ailurose.github.io/aishi/'
        myEmbed = discord.Embed(
            title="Github",
            description=
            "Thank you for being interested in our github!\n\nHere is the link, which contains the link to invite the bot to other servers: "
            + githublink,
            color=color)
        await message.channel.send(embed=myEmbed)

    ### pick command: makes a choice for you
    @commands.command()
    async def pick(self, message, *, choices):
        orSign = '|'
        choiceSplit = choices.split('|')
        if orSign in choices and len(choiceSplit) > 1:
            selection = random.sample(choiceSplit, 1)[0]
            myEmbed = discord.Embed(title="",
                                    description="Aishi picks " +
                                    selection.strip() + "!",
                                    color=color)
        else:
            myEmbed = discord.Embed(
                title="",
                description=
                "**Please provide at least two items for me to pick!**\n`~pick peach | potato` will get me to pick between peach and potato!",
                color=color)
        await message.channel.send(embed=myEmbed)

    ### servers command: displays the amount of servers Aishi is in
    @commands.command()
    async def servers(self, message):
        myEmbed = discord.Embed(
            title="",
            description="Proudly providing love and care to " +
            str(len(self.bot.guilds)) + " servers! ❤️",
            color=color)
        await message.channel.send(embed=myEmbed)

    ### members command: displays the total amount of users using Aishi
    @commands.command()
    async def members(self, message):
        membercount = 0
        activeServers = self.bot.guilds
        for s in activeServers:
            membercount += len(s.members)
        myEmbed = discord.Embed(
            title="",
            description="Proudly providing love and care to " +
            str(membercount) + " members! ❤️",
            color=color)
        await message.channel.send(embed=myEmbed)

    ### newegg shuffle command: newegg shuffle notification system
    @commands.command()
    async def shuffleegg(self, ctx):
        myEmbed = discord.Embed(
            title="Newegg Shuffle",
            description=
            "This command is to sign up for notification via DM anytime Newegg tweets about the next Newegg shuffle.",
            color=color)
        myEmbed.add_field(
            name="Start",
            value=
            "To confirm that you want to sign up for this, please type `start`"
        )
        myEmbed.add_field(
            name="Stop",
            value="To stop getting Newegg Shuffle DMs, please type `stop`")
        myEmbed.add_field(name="Exit",
                          value="Otherwise, type `exit` to exit this menu.")
        await ctx.channel.send(embed=myEmbed)

        def check(m):
            return (m.content.lower() == 'start' or m.content.lower() == 'stop'
                    or m.content.lower()
                    == 'exit') and m.author.id == member.id

        try:
            msg = await self.bot.wait_for("message", timeout=10, check=check)
        except asyncio.TimeoutError:
            await ctx.channel.send(
                "Newegg shuffle menu has timed out due to inactivity")
        else:
            member = ctx.guild.get_member(ctx.author.id)
            memberid = ctx.author.id
            if msg.content.lower() == 'start':
                info = data('egg', 'create', memberid)
                if info == 'done':
                    await member.send(
                        "You are already subscribbed to the Newegg shuffle notification system. Aishi will do her best to continue her services to you."
                    )
                elif info != 'error':
                    await member.send(
                        "Thank you for subscribing to the Newegg shuffle notification system. Aishi make sure to send you the most recent shuffle whenever it is tweeted out!"
                    )
                else:
                    await member.send(
                        "Sorry, Aishi cannot put you on the notification list at this time... please try again later!"
                    )
            elif msg.content.lower() == 'stop':
                info = data('egg', 'deleteall', memberid)
                if info != 'error':
                    await member.send(
                        "I'm sorry to hear that you no longer want to receive Aishi's shuffle notifications. You are no longer a part of the notification list now"
                    )
                else:
                    await member.send(
                        "Sorry, Aishi cannot unsubscribe you from the notification system at this time... please try again later!"
                    )
            elif msg.content.lower() == 'exit':
                return
            await msg.delete()

    ### headpet command: generates headpet
    @commands.command()
    async def petpet(self, ctx, member=''):
        mentionFormat = "<@"
        try:
            memberid = ''
            for word in list(member):
                if word.isdigit():
                    memberid += word
            member = ctx.guild.get_member(int(memberid))
            userpfp = requests.get(member.avatar_url)
            source = BytesIO(userpfp.content)
            source.seek(0)
            dest = BytesIO()
            petpetgif.make(source, dest)
            dest.seek(0)
            await ctx.send(file=discord.File(
                dest, filename=member.display_name + '-petpet.gif'))
        except:
            await ctx.channel.send("No petpets were handed out ;w;")

    ### version command: displays the name of the most current version
    @commands.command(name='version', aliases=['ver'])
    async def version(self, ctx):
        version = "CHRISTMAS MIRACLE AISHI UNCAP ver!! Merry Kurisumasu from Aishi!"
        await ctx.channel.send(version)


def setup(bot):
    bot.add_cog(OtherCommands(bot))
