import discord
import os
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
from messages import msgs
from messages import msg1
from keep_alive import keep_alive
from raids import raids
from raids import roles
from api import mmr
from api import twt
from api import data
from api import riot

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='~', help_command=None, intents=intents)
regions = ['na','euw','eune']
color = 0xffb7c5
embed = discord.Embed(title = "", description = "", colour = color)
reaction_message_id = None

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="~help"))
  print("Shiro is cute")
  print(discord.__version__)

'''
admin commands
'''
@bot.command(name = '@makeroles')
@has_permissions(administrator=True)
async def makeroles(message):
  for role_name in list(raids()):
    await message.guild.create_role(name=role_name)
  await message.message.delete()

@bot.command(name = '@deleteroles')
@has_permissions(administrator=True)
async def deleteroles(message, *, role_name):
  role = discord.utils.get(message.guild.roles, name=role_name)
  await role.delete()

@bot.command(name = '@addrole')
@has_permissions(administrator=True)
async def addrole(message, *, role_name):
  await message.guild.create_role(name=role_name)

@bot.command(name = '@gbfroles')
@has_permissions(administrator=True)
async def gbfRoles(message):
  myEmbed = discord.Embed(title = 'Granblue Roles', description = 'Granblue roles have been created! Members can now join roles by using reacting to emojis \n', color = color)
  raid = raids()
  raidNames = list(raid)
  reactions = roles()
  for index in range(len(raidNames)):
    reaction = reactions[index]
    types = raid[raidNames[index]]
    t_str = ''
    for t in types:
      t_str+= t + '\n'
    myEmbed.add_field(name = reaction + ' ' + raidNames[index], value=t_str)
  text = await message.send(embed = myEmbed)

  global reaction_message_id
  reaction_message_id = text.id

  for role in reactions:
    await text.add_reaction(emoji = role)
  await message.message.delete()


@bot.listen('on_raw_reaction_add')
async def add_role(payload: discord.RawReactionActionEvent):
  if payload.user_id == bot.user.id:
    return

  if reaction_message_id != payload.message_id:
    return

  reactions = roles()
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

  reactions = roles()
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
easter egg commands
'''
@bot.command(name='aiwu')
async def ailu_cuter(message):
  aiwu_def = msg1()
  if message.author != bot.user:
    await message.channel.send(random.sample(aiwu_def, 1)[0])

@bot.command(name='shiwo')
async def shiro_cute(message):
  shiro_def = msgs()
  if message.author != bot.user:
    await message.channel.send(random.sample(shiro_def, 1)[0])

'''
help commands
'''
@bot.group(invoke_without_command=True)
async def help(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = 'Commands', description = 'Type `~help <command>` for more help eg. `~help ammr`', color = color)
    myEmbed.add_field(name = 'Granblue', value = '`raid`')
    myEmbed.add_field(name = 'League', value = '`ammr`\n`aram`')
    myEmbed.add_field(name = 'Profile', value = '`~pfp`')
    myEmbed.set_footer(text="Type ~@help for mod commands")
    await message.channel.send(embed = myEmbed)

@help.command()
async def raid(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = 'GBF Raid', description = '`~raid <user>` sends the GBF raid tweet from specified twitter user', color = color)
    await message.channel.send(embed = myEmbed)

@help.command()
async def ammr(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = "Aram MMR Help", description = '`~ammr <user> <region>` lists summoner ARAM MMR \n\n**regions**\n`na = north america`\n`euw = EU West`\n`eune = EU Nordic & East`\n\nnote: default region is na', color = color)
    await message.channel.send(embed = myEmbed)

@help.command()
async def pfp(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = "Profile Help", description = '`~pfp` provides the profile of the user with any game codes that have been added by the user', color = color)
    myEmbed.add_field(name = '***Examples***', value = '`~pfp`\nshows your own profile card\n\n`~pfp @Teru#4584`\nshows Teru profile card\n\n`~pfp add title description`\nadds to your profile an element with the selected title and description\n\n`~pfp add "Are hammys cute?" "Yes, of course"`\nadds to your profile an element with the title being "Are hammys cute" and the description being "Yes, of course"\n\n`~pfp delete title`\ndeletes selected title from your profile card\n\n`~deleteall`\nclears your entire profile card')
    myEmbed.add_field(name = '***Usages***', value = '`~pfp [add <title> <description> | delete <title> | deleteall]`')
    await message.channel.send(embed = myEmbed)

@bot.group(invoke_without_command = True, name = '@help')
async def mod_help(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = 'Moderator Commands', description = 'Type `~@help <command> for more help eg. `~@help gbfroles', color = color)
    myEmbed.add_field(name = 'Granblue', value = '`gbfroles`\n`makeroles`\n`addrole`\n`deleteroles`')
    await message.channel.send(embed = myEmbed)

@mod_help.command()
async def gbfroles(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = 'GBF Roles', description = '`~@gbfroles` lists the created roles for raids and allows server members to join by reacting. Server members cannot join roles until `~@makeroles` command has been called', color = color)
    myEmbed.add_field(name = 'Related Commands', value = '`makeroles`\n`addrole`\n`deleteroles`')
    await message.channel.send(embed = myEmbed)

@mod_help.command()
async def makeroles(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = 'Make GBF Roles', description = '`~@makeroles` creates all roles for raids to be reacted when `~@gbfroles` is called', color = color)
    myEmbed.add_field(name = 'Related Commands', value = '`gbfroles`\n`addrole`\n`deleteroles`')
    await message.channel.send(embed = myEmbed)

@mod_help.command()
async def addrole(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = 'Add GBF Role', description = '`~@addrole <role>` allows for the creation of individual roles to be added for raids ', color = color)
    myEmbed.add_field(name = 'Related Commands', value = '`gbfroles`\n`makeroles`\n`deleteroles`')
    await message.channel.send(embed = myEmbed)

@mod_help.command()
async def deleteroles(message):
  if message.author != bot.user:
    myEmbed = discord.Embed(title = 'Delete GBF Roles', description = '`~@deleteroles <role>` allows for the deletion of individual roles associated to raids', color = color)
    myEmbed.add_field(name = 'Related Commands', value = '`gbfroles`\n`makeroles`\n`addrole`')
    await message.channel.send(embed = myEmbed)

'''
granblue fantasy commands
'''
@bot.command()
async def raid(message, user=''):
  if user == '':
    myEmbed = discord.Embed(title = "", description = "No twitter username input. Please input twitter username", color = color)
    await message.channel.send(embed = myEmbed)
  elif message.author != bot.user:
    battleID, raidName, msg = twt(user)
    checker = ':Battle ID\nI need backup!'
    if checker in msg:
      raid = raids()
      for r in raid:
        for types in raid[r]:
          if raidName in types:
            try:
              ping = get(message.guild.roles, name = r)
              await message.channel.send(ping.mention)
            except AttributeError:
              myEmbed = discord.Embed(title = "", description = "", color = color)
      myEmbed = discord.Embed(title = "", description = msg, color = color)
    else:
      myEmbed = discord.Embed(title = "", description = 'There are no recent raid msgs from ' + user, color = color)
    await message.channel.send(embed = myEmbed)
    await message.channel.send(battleID)

'''
league commands
'''
@bot.command()
async def ammr(message, user='', region='na'):
  if user == '':
    myEmbed = discord.Embed(title = "", description = "No summoner input. Please input summoner name", color = color)
    await message.channel.send(embed = myEmbed)
  elif user.lower() == 'glancelot':
    myEmbed = discord.Embed(title = "", description = user + "'s mmr is: 42069", color = color)
    await message.channel.send(embed = myEmbed)
  elif (message.author != bot.user):
    if region in regions:
      aram = mmr(user, 'ARAM', region)
      if aram == 'error':
        myEmbed = discord.Embed(title = "", description = "There is no ARAM data on this user", color = color)
        await message.channel.send(embed = myEmbed)
      else:
        myEmbed = discord.Embed(title = "", description = user + "'s mmr is: " + str(aram), color = color)
        await message.channel.send(embed = myEmbed)
    else:
      myEmbed = discord.Embed(title = "", description = "Invalid region. Please input one of the following regions when calling the command: \n\t`na = north america`\n\t`euw = EU West`\n\t`eune = EU Nordic & East`", color = color)
      await message.channel.send(embed = myEmbed)

@bot.command()
async def aram(message, user, region='na'): 
  teams = riot(user, 'ARAM', region)
  if teams != 'error':
    yourTeam = ''
    enemyTeam = ''
    teamsList = ['team1', 'team2']
    for team in teamsList:
      for players in teams[team]:
        mmrNum = str(players[1])
        if mmrNum == 'error':
          mmrNum = 'N/A'
        if team == teams['playerTeam']:
          yourTeam = yourTeam + '*' + players[0] + '*  :  ' + '\t\t\t' + str(players[1]) + '\n'
        else:
          enemyTeam = enemyTeam + '*' + players[0] + '*  :  ' + '\t\t\t' + str(players[1]) + '\n'
    myEmbed = discord.Embed(title = "ARAM mmr", description = "", color = color)
    myEmbed.add_field(name = "Your Team", value = yourTeam)
    myEmbed.add_field(name = "Enemy Team", value = enemyTeam, inline = False)
  else:
    myEmbed = discord.Embed(title = "", description = "There are no current ARAM games with " + user, color = color)      
  await message.channel.send(embed = myEmbed)

'''
profile stuff
'''

@bot.group(invoke_without_command=True)
async def pfp(message, member = ''):
  mentionFormat = "<@"
  print(member)
  if member == '':
    member = message.guild.get_member(message.author.id)
    memberid = message.author.id
  elif mentionFormat in member:
    memberid = member.split(mentionFormat)[1].split('!')[1].split('>')[0]
    member = message.guild.get_member(int(memberid))
  else:
    myEmbed = discord.Embed(title = "", description = "This user does not exist", color = color)
    await message.send(embed = myEmbed)
    return
  myEmbed = discord.Embed(title = "", description = "", color = color)
  myEmbed.set_author(name = f"User Info = {member}")
  myEmbed.set_thumbnail(url = member.avatar_url)
  myEmbed.set_footer(text = f"Requested by {message.author}", icon_url = message.author.avatar_url)
  myEmbed.add_field(name = "Username:", value = member.display_name)
  info = data('read', memberid)
  if info != 'error':
    for i in info['games']:
      myEmbed.add_field(name = i.capitalize(), value = info['games'][i], inline=False)
  await message.send(embed = myEmbed)

@pfp.command()
async def add(message, game, code):
  gameCode = {game.lower(): code}
  info = data('create', message.author.id, gameCode)
  if info != 'error':
    myEmbed = discord.Embed(title = "", description = "Your game code has been added to your profile", color = color)
  else:
    myEmbed = discord.Embed(title = "", description = "Your game code was not added to your profile", color = color)
  await message.channel.send(embed = myEmbed)

@pfp.command()
async def deleteall(message):
  data('deleteall', message.author.id)
  myEmbed = discord.Embed(title = "", description = "Your profile data has been cleared", color = color)
  await message.channel.send(embed = myEmbed)

@pfp.command()
async def delete(message, game):
  info = data('delete', message.author.id, game.lower())
  if info != 'error':
    myEmbed = discord.Embed(title = "", description = "The requested data has been cleared", color = color)
  else:
    myEmbed = discord.Embed(title = "", description = "The requested data was not cleared", color = color)
  await message.channel.send(embed = myEmbed)


token = os.environ.get("DISCORD_BOT_SECRET")
keep_alive()
bot.run(token)