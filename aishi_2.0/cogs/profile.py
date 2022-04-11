import discord, os
from discord.ext import commands
from api import data

color = 0xffb7c5


class ProfileCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #original profile commands
    '''
    @bot.group(invoke_without_command=True)
    async def pfp(message, member=''):
      mentionFormat = "<@"
      if member.lower() == 'aishi':
        myEmbed = discord.Embed(title="",
                                description="You actually want to know about me? :pleading_face:", color=color)
        myEmbed.set_author(name="User Info = Aishi Bot")
        myEmbed.set_footer(text=f"Requested by {message.author}", icon_url=message.author.avatar_url)
      else:
        if member == '':
          member = message.guild.get_member(message.author.id)
          memberid = message.author.id
        elif mentionFormat in member:
          memberid = member.split(mentionFormat)[1].split('!')[1].split('>')[0]
          member = message.guild.get_member(int(memberid))
        else:
          myEmbed = discord.Embed(title="",
                                  description="This user does not exist",color=color)
          await message.send(embed=myEmbed)
          return
    
        myEmbed = discord.Embed(title="", description="", color=color)
        myEmbed.set_author(name=f"User Info = {member}")
        myEmbed.set_thumbnail(url=member.avatar_url)
        myEmbed.set_footer(text=f"Requested by {message.author}", icon_url=message.author.avatar_url)
        myEmbed.add_field(name="Username:", value=member.display_name)
        info = data('read', memberid)
        if memberid == "146437419418255361":
          myEmbed.add_field(name="Bandage:",
                            value = "Aishi realized that your data has been lost. Here is a bandage :<", inline = False)
        elif info != 'error':
              for i in info['games']:
                  myEmbed.add_field(name=i.capitalize(), value=info['games'][i], inline=False)
        await message.send(embed=myEmbed)
    
    
    @pfp.command()
    async def add(message, game, code):
    	gameCode = {game.lower(): code}
    	info = data('create', message.author.id, gameCode)
    	if info != 'error':
    		myEmbed = discord.Embed(
    		    title="",
    		    description="Your data has been added to your profile",
    		    color=color)
    	else:
    		myEmbed = discord.Embed(
    		    title="",
    		    description="Your data was not added to your profile",
    		    color=color)
    	await message.channel.send(embed=myEmbed)
    
    
    @pfp.command()
    async def delete(message, game):
    	info = data('delete', message.author.id, game.lower())
    	if info != 'error':
    		myEmbed = discord.Embed(
    		    title="",
    		    description="The requested data has been cleared",
    		    color=color)
    	else:
    		myEmbed = discord.Embed(
    		    title="",
    		    description="The requested data was not cleared",
    		    color=color)
    	await message.channel.send(embed=myEmbed)
    
    
    @pfp.command()
    async def deleteall(message):
    	data('deleteall', message.author.id)
    	myEmbed = discord.Embed(title="", description="Your profile data has been cleared", color=color)
    	await message.channel.send(embed=myEmbed)
    '''
    #new profile commands

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pfp(self, message, member=''):
        mentionFormat = "<@"
        if member.lower() == 'aishi' or (
                member != ''
                and member.split(mentionFormat)[1].split('!')[1].split('>')[0]
                == str(os.environ.get("BOT_ID"))):
            myEmbed = discord.Embed(
                title="",
                description=
                "You actually want to know about me? :pleading_face:",
                color=color)
            myEmbed.set_author(name="User Info = Aishi Bot")
            member = message.guild.get_member(int(os.environ.get("BOT_ID")))
            myEmbed.set_thumbnail(url=member.avatar_url)
            myEmbed.set_footer(text=f"Requested by {message.author}",
                               icon_url=message.author.avatar_url)
            await message.send(embed=myEmbed)
        else:
            if member == '':
                member = message.guild.get_member(message.author.id)
                memberid = message.author.id
            elif mentionFormat in member:
                memberid = ''
                for word in list(member):
                    if word.isdigit():
                        memberid += word
                member = message.guild.get_member(int(memberid))
            else:
                myEmbed = discord.Embed(title="",
                                        description="This user does not exist",
                                        color=color)
                await message.send(embed=myEmbed)
                return

            myEmbed = discord.Embed(title="", description="", color=color)
            myEmbed.set_author(name=f"User Info = {member}")
            myEmbed.set_thumbnail(url=member.avatar_url)
            myEmbed.set_footer(text=f"Requested by {message.author}",
                               icon_url=message.author.avatar_url)
            myEmbed.add_field(name="Username:", value=member.display_name)
            info = data('profile', 'read', memberid)
            if info != 'error':
                for i in info['labels']:
                    myEmbed.add_field(name=i.capitalize(),
                                      value=info['labels'][i],
                                      inline=False)
            await message.send(embed=myEmbed)

    @pfp.command()
    async def add(self, message, game='', code=''):
        gameCode = {game.lower(): code}
        info = data('profile', 'create', message.author.id, gameCode)
        if info != 'error':
            myEmbed = discord.Embed(
                title="",
                description="Your data has been added to your profile",
                color=color)
        else:
            myEmbed = discord.Embed(
                title="",
                description="Your data was not added to your profile",
                color=color)
        await message.channel.send(embed=myEmbed)

    @pfp.command()
    async def delete(self, message, game):
        info = data('profile', 'delete', message.author.id, game.lower())
        if info != 'error':
            myEmbed = discord.Embed(
                title="",
                description="The requested data has been cleared",
                color=color)
        else:
            myEmbed = discord.Embed(
                title="",
                description="The requested data was not cleared",
                color=color)
        await message.channel.send(embed=myEmbed)

    @pfp.command()
    async def deleteall(self, message):
        info = data('profile', 'deleteall', message.author.id)
        if info != 'error':
            myEmbed = discord.Embed(
                title="",
                description="Your profile data has been cleared",
                color=color)
        else:
            myEmbed = discord.Embed(
                title="",
                description=
                "Your profile data couldn't be cleared. Please try again.",
                color=color)
        await message.channel.send(embed=myEmbed)


def setup(bot):
    bot.add_cog(ProfileCommands(bot))
