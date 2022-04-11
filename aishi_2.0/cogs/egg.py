import asyncio, discord, nums_from_string, random
from discord.ext import commands
from messages import msgs, msg1, msg2

counter = [0, 0, 0, 0, 0]
color = 0xffb7c5


class EggCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ### listens for certain keywords and responds with fun easter egg
    @commands.Cog.listener("on_message")
    async def message_listener(self, message):
        keywords = {
            "dee mention":
            "https://cdn.discordapp.com/attachments/790381448862629929/962848881236922378/unknown.png",
            "janie mention":
            "https://cdn.discordapp.com/attachments/790381448862629929/962853478521241640/unknown.png",
            "hien mention":
            "https://tenor.com/view/apple-cat-fast-gif-19997541",
            "zeph mention":
            "https://tenor.com/view/gbf-zephyrus-zephium-gif-20336716",
            "hiencarry mention":
            "https://cdn.discordapp.com/attachments/728451357748756510/921570248925249586/B4B576A7-ACFD-496F-8FFD-119AAEE939B5.png",
            "reason carry":
            "https://cdn.discordapp.com/attachments/728451357748756510/956688637599301702/unknown.png",
            "el racho":
            "https://media.discordapp.net/attachments/377842793160376320/935604917471698944/kangel1.gif",
            "el ration":
            "don't care + didn't ask + cry about it + stay mad + get real + L + mald + seethe + cope harder + hoes mad + basic + skill issue + ratio + you fell off + the audacity + triggered + any askers + red pilled + get a life + ok and? + cringe + go touch grass + donowalled + not based + you're probably white + not funny didn't laugh + grammar issue + go outside + get good + reported + ad hominem + GG! + ur mom + blocked"
        }  # "shut the fuck up": "no king uwu https://cdn.discordapp.com/emojis/895419550407995403.png?size=128"}
        user_ids = [
            587791779265380362, 242876953701384192, 272352511677956098,
            143932697792741376, 153352075357454336
        ]
        messages = [
            'aiwu cute', 'hi king', 'explode', 'silverchou banzai',
            'shiwo pwecious'
        ]
        hien_def = msg2()
        if message.author != self.bot.user:
            if "if hien" in message.content.lower():
                msg = 'if hien has million number of fans i am one of them. if hien has ten fans i am one of them. if hien has no fans that means i am no more on the earth. if world against hien , i am against the world. i love hien till my last breath... die hardfan of hien . Hit like if u think hien best & smart in the lightmain, windmain, firemain, watermain, sexymain 😳'
                return await message.channel.send(msg)
            for keyword in keywords:
                if keyword in message.content.lower():
                    if keyword == 'hien mention':
                        my_list = ['A'] * 80 + ['B'] * 19 + ['C'] * 1
                        choice = random.choice(my_list)
                        if choice == 'A':
                            await message.channel.send(
                                random.sample(hien_def, 1)[0])
                            await message.channel.send(keywords[keyword])
                        elif choice == 'B':
                            await message.channel.send(
                                random.sample(hien_def, 1)[0])
                            await message.channel.send(
                                'https://tenor.com/view/apple-apple-cat-shut-up-gif-23299005'
                            )
                        elif choice == 'C':
                            await message.channel.send('you called?')
                            await message.channel.send(
                                'https://cdn.discordapp.com/emojis/895419550407995403.webp?size=96&quality=lossless'
                            )
                    else:
                        await message.channel.send(keywords[keyword])
            for index in range(len(user_ids)):
                if message.author.id == user_ids[index]:
                    counter[index] += 1
                    if counter[index] == 30:
                        if message.author.id == 153352075357454336:
                            if message.guild.id == 782329997477543936:
                                print("test works")
                                counter[index] = 0
                                return await message.channel.send(
                                    messages[index])
                            else:
                                return
                        await message.channel.send(messages[index])
                        if message.author.id == 143932697792741376:
                            await asyncio.sleep(5)  #sleep method timer
                            await message.channel.send('.')
                        counter[index] = 0

    ### aiwu is cute command
    @commands.command(name='aiwu')
    async def ailu_cuter(self, message):
        aiwu_def = msg1()
        if message.author != self.bot.user:
            await message.channel.send(random.sample(aiwu_def, 1)[0])

    ### shiwo is cute command
    @commands.command(name='shiwo')
    async def shiro_cute(self, message):
        shiro_def = msgs()
        if message.author != self.bot.user:
            await message.channel.send(random.sample(shiro_def, 1)[0])

    ### giveaway command !!! must fix later
    @commands.command(name='giveaway')
    async def gcreate(self, message, gtime=None, *, prize=None):
        if gtime == None:
            return await message.send('Please include a time')
        elif prize == None:
            return await message.send('Please include a prize')
        try:
            myEmbed = discord.Embed(
                title='New Giveaway~',
                description=
                f'{message.author.mention} is giving away **{prize}**',
                color=color)
            time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            gatime = int(
                nums_from_string.get_nums(gtime)[0]) * time_convert[gtime[-1]]
            myEmbed.set_footer(text=f'Giveaway ends in {gtime}')
            ga_msg = await message.channel.send(embed=myEmbed)

            await ga_msg.add_reaction("🎊")
            await asyncio.sleep(gatime)

            new_ga_msg = await message.channel.fetch_message(ga_msg.id)

            users = await new_ga_msg.reactions[0].users().flatten()
            users.pop(users.index(self.bot.user))

            winner = random.choice(users)

            myEmbed = discord.Embed(
                title="",
                description=
                f"🎊   Congratulations {winner.mention} has won the giveaway for **{prize}**",
                color=color)
            await message.channel.send(embed=myEmbed)
        except:
            await message.channel.send(
                "The giveaway format is incorrect. Please recheck your message and try again."
            )

    '''
    @commands.command(name='gacha')
    async def gacha(self, message):'''


def setup(bot):
    bot.add_cog(EggCommands(bot))
