import discord
import os, re
import tweepy
from itertools import cycle
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
from discord.utils import get
import asyncio
from keep_alive import keep_alive
from raids import raids, gbfroles
from api import twt, data
import nums_from_string

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='~',
                   help_command=None,
                   intents=intents,
                   case_insensitive=True)
status = cycle(['~help', 'gamers'])
regions = ['na', 'euw', 'eune']
color = 0xffb7c5
reaction_message_id = None
counter = [0, 0, 0, 0, 0]


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name='~help'))
    checkegg.start()
    #checkremind.start()
    print("Shiro is cute")
    print(discord.__version__)


#bg task that should hopefully keep it alive
#@tasks.loop(seconds=10)
#async def change_status():
#await bot.change_presence(activity=discord.Game(next(status)))
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next(status)))


#checks for newegg message
@tasks.loop(seconds=10)
async def checkegg():
    info = twt('egg', 'newegg')
    if info is not None:
        memberids = data('egg', 'read')
        if memberids != 'error':
            for memberid in memberids:
                found = False
                for guild in bot.guilds:
                    if found == True:
                        continue
                    for member in guild.members:
                        if member.id == int(memberid):
                            myEmbed = discord.Embed(title="NewEgg Shuffle",
                                                    description=info,
                                                    color=color)
                            await member.send(embed=myEmbed)
                            found = True


#@tasks.loop(seconds=10)
@bot.command(name='cr')
async def checkremind(ctx):
    info, current = data('remind', 'readall')
    print(info)
    print(current)
    print('-------------------------')
    if info != 'error':
        print("BRRRING ALARM")


#error handler
@bot.event
async def on_command_error(message, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        msg = '**' + str(message.author).split(
            '#')[0] + '**, please cool down! ({:.2f}s)'.format(
                error.retry_after)
        await message.send(msg, delete_after=5)
    print(str(error))


'''
admin commands
'''


## granblue admin commands
@bot.command(name='@makeroles')
@has_permissions(administrator=True)
async def makeroles(message):
    for role_name in list(raids()):
        await message.guild.create_role(name=role_name)
    await message.message.delete()


@bot.command(name='@deleteroles')
@has_permissions(administrator=True)
async def deleteroles(message, *, role_name):
    role = discord.utils.get(message.guild.roles, name=role_name)
    await role.delete()


@bot.command(name='@addrole')
@has_permissions(administrator=True)
async def addrole(message, *, role_name):
    await message.guild.create_role(name=role_name)


'''
granblue fantasy commands
'''


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def raid(message, user=''):
    if user == '':
        myEmbed = discord.Embed(
            title="",
            description=
            "No twitter username input. Please input twitter username",
            color=color)
        await message.channel.send(embed=myEmbed)
    elif message.author != bot.user:
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
                myEmbed = discord.Embed(title="", description=msg, color=color)
            else:
                myEmbed = discord.Embed(
                    title="",
                    description='There are no recent raid msgs from ' + user,
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


@bot.command(name='gbfroles')
async def gbfRoles(message):
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
        myEmbed.add_field(name=reaction + ' ' + raidNames[index], value=t_str)
    text = await message.send(embed=myEmbed)

    global reaction_message_id
    reaction_message_id = text.id

    for role in reactions:
        await text.add_reaction(emoji=role)
    await message.message.delete()


@bot.listen('on_raw_reaction_add')
async def add_role(payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return

    if reaction_message_id != payload.message_id:
        return

    reactions = gbfroles()
    reaction = payload.emoji.name
    if reaction not in reactions:
        return

    role_names = list(raids())
    role_name = role_names[reactions.index(reaction)]
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = discord.utils.get(guild.roles, name=role_name)
    await member.add_roles(role)


@bot.listen('on_raw_reaction_remove')
async def remove_role(payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return

    if reaction_message_id != payload.message_id:
        return

    reactions = gbfroles()
    reaction = payload.emoji.name
    if reaction not in reactions:
        return

    role_names = list(raids())
    role_name = role_names[reactions.index(reaction)]
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = discord.utils.get(guild.roles, name=role_name)
    await member.remove_roles(role)


'''
Task Helper
'''


@bot.group(invoke_without_command=True)
async def task(message):
    member = message.guild.get_member(message.author.id)
    memberid = message.author.id
    myEmbed = discord.Embed(title="", description="", color=color)
    myEmbed.set_author(name=f"Task Helper")
    myEmbed.set_thumbnail(url=member.avatar_url)
    myEmbed.set_footer(text=f"Requested by {message.author}",
                       icon_url=message.author.avatar_url)
    myEmbed.add_field(name="Username:", value=member.display_name)
    #info = data('task', 'read', memberid)
    #if info != 'error':
    #  for i in info['labels']:
    #    myEmbed.add_field(name=i.capitalize(), value=info['labels'][i], inline=False)
    await message.send(embed=myEmbed)


@task.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def remind(ctx, action=''):
    allactions = {
        'Add': 'adds your personalized reminder',
        'Delete': 'deletes the reminder of your choice',
        'Deleteall': 'removes all reminders that you have set',
        'Edit': 'edits a pre-existing reminder'
    }
    member = ctx.guild.get_member(ctx.author.id)
    memberid = ctx.author.id

    def check(m):
        checker = False
        for act in allactions:
            checker = checker or m.content.lower() == act.lower()
        return checker and m.author.id == memberid

    def check2(m):
        symbols = ['-', '.']
        splitter = m.content.split(' ')
        checker = m.author.id == memberid
        signTrue = '+' in m.content or '-' in m.content
        for index in range(len(symbols)):
            checker = checker and symbols[index] in splitter[index]
        return (checker and any(char.isdigit() for char in m.content)
                and signTrue) or m.content.lower() == 'help'

    def check3(m):
        return m.author.id == memberid

    timeoutmsg = "Aishi Reminder menu has timed out due to inactivity"
    if action == '':
        myEmbed = discord.Embed(
            title="Aishi Reminder System",
            description=
            "Welcome to the Aishi Reminder System! Please proceed by typing in one of the following commands or typing `exit` to exit the menu.",
            color=color)
        for action in allactions:
            myEmbed.add_field(name=action,
                              value=allactions[action],
                              inline=False)
        await ctx.channel.send(embed=myEmbed)

        try:
            msg = await bot.wait_for("message", timeout=10, check=check)
        except asyncio.TimeoutError:
            await ctx.channel.send(timeoutmsg)
        else:
            if msg.content.lower() == 'exit':
                return
            else:
                action = msg.content.lower()
    if action != '':
        if action == 'add':
            await ctx.channel.send("Please enter the title of the reminder")
            try:
                titleremind = await bot.wait_for("message",
                                                 timeout=360,
                                                 check=check3)
            except asyncio.TimeoutError:
                await ctx.channel.send(timeoutmsg)
            else:
                await ctx.channel.send(
                    "Please enter a time you would like to be reminded (or type `help` for assistance): "
                )
                try:
                    timeremind = await bot.wait_for("message",
                                                    timeout=360,
                                                    check=check2)
                except asyncio.TimeoutError:
                    await ctx.channel.send(timeoutmsg)
                else:
                    if timeremind.content == 'help':
                        myEmbed = discord.embed(
                            title='Help Setting Remind Time',
                            description=
                            'Please use one of the following methods to set your reminder: '
                        )
                        myEmbed.add_field(
                            name='Specific date and time',
                            value=
                            'year-month-day hour.minute:second timezone\n\n*Example: 2021-05-20 20:00:00'
                        )
                        myEmbed.add_field(
                            name='Specific amount of time',
                            value='[second][minute][day][week][year]')
                        print('help')


#year-month-day hour.minute.second
                    else:
                        if '-' in timeremind.content and '.' in timeremind.content:
                            datalist = [
                                titleremind.content,
                                str(timeremind.content).replace('.', ':'),
                                'dateandtime'
                            ]
                        else:
                            time_convert = {
                                "s": 1,
                                "m": 60,
                                "h": 3600,
                                "d": 86400
                            }
                            remindsecond = int(
                                nums_from_string.get_nums(timeremind.content)
                                [0]) * time_convert[timeremind.content[-1]]
                            datalist = [
                                titleremind.content, remindsecond,
                                'remindsecond'
                            ]
                        info = data('remind', 'create', memberid, datalist)
                        if info == 'error':
                            await ctx.channel.send(
                                "I'm sorry but your reminder cannot be added at this time. Please try again later!"
                            )
                        elif info == 'formaterror':
                            await ctx.channel.send(
                                "I'm sorry but your reminder cannot be added due to formatting error. Please check that you have added the reminder time in the right format and try again."
                            )
                        else:
                            await ctx.channel.send(
                                "Your reminder has been added to the system. Thank you for using Aishi task reminder!"
                            )
        elif action == 'delete':
            await ctx.channel.send(
                "Please enter the title of the reminder you would like to delete"
            )
            try:
                timeremind = await bot.wait_for("message",
                                                timeout=360,
                                                check=check3)
            except asyncio.TimeoutError:
                await ctx.channel.send(timeoutmsg)
            else:
                info = data('remind', 'delete', memberid, timeremind.content)
                if info == 'error':
                    await ctx.channel.send(
                        "I'm sorry but your reminder cannot be deleted at this time. Please try again later!"
                    )
                else:
                    await ctx.channel.send("Your reminder has been deleted.")
        elif action == 'deleteall':
            info = data('remind', 'deleteall', memberid)
            if info != 'error':
                await ctx.channel.send("Your reminders have all been cleared")
            else:
                await ctx.channel.send(
                    "Your reminders couldn't be cleared. Please try again.")

extensions = [
    'cogs.egg', 'cogs.genshin', 'cogs.help', 'cogs.league',
    'cogs.other', 'cogs.profile'
]
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"error while loading {extension}")
            print(str(e))

token = os.environ.get("DISCORD_BOT_SECRET")
keep_alive()
bot.run(token)
