import discord
from discord.ext import commands

color = 0xffb7c5


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='Commands',
                description=
                'Type `~help <command>` for more help eg. `~help ammr`',
                color=color)
            myEmbed.add_field(name='Granblue', value='`raid`\n`gbfroles`')
            myEmbed.add_field(name='League', value='`ammr`\n`aram`')
            myEmbed.add_field(name='Genshin', value='`craft`')
            myEmbed.add_field(name='Profile', value='`pfp`')
            myEmbed.add_field(
                name='Miscellaneous',
                value=
                '`feedback`\n`flip`\n`github`\n`petpet`\n`pick`\n`servers`\n`shuffleegg`'
            )
            myEmbed.set_footer(text="Type ~@help for mod commands")
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def raid(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='GBF Raid Help',
                description=
                '`~raid <user>` sends the GBF raid tweet from specified twitter user',
                color=color)
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def ammr(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Aram MMR Help",
                description=
                '`~ammr <user> <region>` lists summoner ARAM MMR \n\n**regions**\n`na = north america`\n`euw = EU West`\n`eune = EU Nordic & East`\n\nnote: default region is na',
                color=color)
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def aram(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Aram Team MMR Help",
                description=
                '`~aram <user> lists ARAM MMR of each summoner in game with specified summoner.',
                color=color)
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def gbfroles(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='GBF Roles Help',
                description=
                '`~@gbfroles` lists the created roles for raids and allows server members to join by reacting. Server members cannot join roles until `~@makeroles` command has been called by admin',
                color=color)
            myEmbed.add_field(name='Related Commands',
                              value='`makeroles`\n`addrole`\n`deleteroles`')
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def craft(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='Genshin Craft Help',
                description=
                '`~craft <blue | purple | gold> <green amount> <blue amount> <purple amount>` performs material calculations for your genshin needs. Input in the material you need and the bot will state how much total you will have if you synthesized all your materials toward that material. Colors are based on the background color of the item.',
                color=color)
            myEmbed.add_field(
                name='***Examples***',
                value=
                '`~craft blue 6`\nWith your materials, you can make a total of 2 blue materials\n\n`~craft gold 2 3`\nWith your materials, you can make a total of 0 gold materials\n\n`~craft purple 0 14 9`\nWith your materials, you can make a total of 13 purple materials'
            )
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def pfp(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Profile Help",
                description=
                '`~pfp` provides the profile of the user with any information that have been added by the user',
                color=color)
            myEmbed.add_field(
                name='***Examples***',
                value=
                '`~pfp`\nshows your own profile card\n\n`~pfp @Teru#4584`\nshows Teru profile card\n\n`~pfp add title description`\nadds to your profile an element with the selected title and description\n\n`~pfp add "Are hammys cute?" "Yes, of course"`\nadds to your profile an element with the title being "Are hammys cute" and the description being "Yes, of course"\n\n`~pfp delete title`\ndeletes selected title from your profile card\n\n`~deleteall`\nclears your entire profile card'
            )
            myEmbed.add_field(
                name='***Usages***',
                value=
                '`~pfp [add <title> <description> | delete <title> | deleteall]`'
            )
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def feedback(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Feedback Help",
                description=
                "`~feedback` allows for all users of aishibot the opportunity to provide feedback. Please use this command to provide any feedback about Aishi!",
                color=color)
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def flip(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Coin Flip Help",
                description=
                '`~flip` allows the user to flip a coin and will return heads or tails',
                color=color)
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def github(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Github Help",
                description=
                "`~github` provides a link directly to the github of the discord bot, containing the bot's invite link as well as a thorough list of the commands",
                color=color)
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def pick(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Pick Help",
                description=
                "`~pick` helps make a choice for you based on the choice you provide Aishi.",
                color=color)
            myEmbed.add_field(
                name='***Examples***',
                value=
                "`~pick potato | peach` \nselects between potato and peach\n\n`~pick dogs are cute | cats are cute | hammies are cute`\n selects between the phrases dogs are cute, cats are cute, and hammies are cute"
            )
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def petpet(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Petpet Help",
                description=
                "`~petpet` allows you to generate a headpetting meme using the profile of the person you mention",
                color=color)
            myEmbed.add_field(
                name='***Exmaple***',
                value="`~petpet @aishi`\ncreates a headpet meme of Aishi")
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def remind(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Remind Help",
                description=
                "`~remind` is a system in which allows users to set up reminders based on a set date or set amount of time"
            )
            myEmbed.add_field(
                name='***Examples***',
                value=
                '`~remind`\nshows all your reminders\n\n`~remind`\nshows Teru profile card\n\n`~pfp add title description`\nadds to your profile an element with the selected title and description\n\n`~pfp add "Are hammys cute?" "Yes, of course"`\nadds to your profile an element with the title being "Are hammys cute" and the description being "Yes, of course"\n\n`~pfp delete title`\ndeletes selected title from your profile card\n\n`~deleteall`\nclears your entire profile card'
            )
            myEmbed.add_field(
                name='***Usages***',
                value=
                '`~pfp [add <title> <description> | delete <title> | deleteall]`'
            )
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def shuffleegg(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Newegg Shuffle Help",
                description=
                "`~shuffleegg` is a notification free subscription system in which allows those who subscribes to be notified whenever newegg tweets about the next shuffle",
                color=color)
            await message.channel.send(embed=myEmbed)

    @help.command()
    async def servers(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title="Servers Help",
                description=
                "`~servers` displays the number of servers that Aishi is on! I'm so happy to be providing love and care to these servers!",
                color=color)
            await message.channel.send(embed=myEmbed)

    @commands.group(invoke_without_command=True, name='@help')
    async def mod_help(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='Moderator Commands',
                description=
                'Type `~@help <command> for more help eg. `~@help gbfroles',
                color=color)
            myEmbed.add_field(name='Granblue',
                              value='`makeroles`\n`addrole`\n`deleteroles`')
            await message.channel.send(embed=myEmbed)

    @mod_help.command()
    async def makeroles(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='Make GBF Roles',
                description=
                '`~@makeroles` creates all roles for raids to be reacted when `~@gbfroles` is called',
                color=color)
            myEmbed.add_field(name='Related Commands',
                              value='`gbfroles`\n`addrole`\n`deleteroles`')
            await message.channel.send(embed=myEmbed)

    @mod_help.command()
    async def addrole(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='Add GBF Role',
                description=
                '`~@addrole <role>` allows for the creation of individual roles to be added for raids ',
                color=color)
            myEmbed.add_field(name='Related Commands',
                              value='`gbfroles`\n`makeroles`\n`deleteroles`')
            await message.channel.send(embed=myEmbed)

    @mod_help.command()
    async def deleteroles(self, message):
        if message.author != self.bot.user:
            myEmbed = discord.Embed(
                title='Delete GBF Roles',
                description=
                '`~@deleteroles <role>` allows for the deletion of individual roles associated to raids',
                color=color)
            myEmbed.add_field(name='Related Commands',
                              value='`gbfroles`\n`makeroles`\n`addrole`')
            await message.channel.send(embed=myEmbed)

    '''
  to be taco
  class Help(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      
    @commands.command(
      name = 'ahelp', aliases = ['h', 'commands'], description = "Aishi's help commands"
    )
  
    async def ahelp(self, ctx, cog = "1"):
      helpEmbed = discord(
        title = "Help commands", color = color
      )
      cogs = [c for c in self.bot.cogs.keys()]
    
      for cog in neededCogs:
        commandList =  ""
        for command in self.bot.get_cog(cog).walk_commands():
          if command.hidden:
            continue
          elif command.parent != None:
            continue
          commandList += f"**{commands.name}** - *{command.description}*"
        commandList += "\n"
  
        helpEmbed.add_field(name = cog, value = commandList, inline = False)
      await ctx.send(embed = helpEmbed)
  '''
def setup(bot):
    bot.add_cog(HelpCommands(bot))