import discord
import help
import luigi
import mario
from youtube import playlist_save
import random as rn
import reactions
import roll

RESPONSES = [
    "cringe",
    "oh brother this STINKS",
    "damn bro, that's kinda cringe",
    "ratio",
    "no <3",
    "user has been banned for 3 hours for posting cringe",
    "cringe detected, deploying tear gas"
]

IMAGES = [
    "images/bottle_cat.jpg",
    "images/new_jersey.jpg",
    "images/jackfilm_cringe.jpg",
    "images/pringle_cringe.jpg",
    "images/cringe_collection.jpg"
]

async def dice_roll_command(message: discord.Message):
    if message.content.startswith("!roll"):
        nat1 = await roll.roll_dice(message, str(message.content))
        if nat1:
            mess, image = rn.choice(RESPONSES), rn.choice(IMAGES)
            await message.channel.send(mess, file=discord.File(image))
        return True

async def amogus_command(message: discord.Message):
    AMONGUS_IMAGES = [
        "images/amongsomebitches.jpg",
        "images/impostersus.jpg"
    ]

    if "among" in message.content.lower() or "amogus" in message.content.lower() or "sus" in message.content.lower() or "imposter" in message.content.lower():
        image = rn.choice(AMONGUS_IMAGES)
        await message.reply("WHEN THE IMPOSTER IS SUS", file=discord.File(image))

async def loss_command(message: discord.Message):
    if "loss" in message.content.lower():
        await message.reply("| l| || |_", file=discord.File("images/loss.jpg"))

async def mario_command(message: discord.Message):
    if "!mario" in message.content.lower():
        await mario.reply(message)

async def luigi_command(message: discord.Message):
    if "!luigi" in message.content.lower():
        await luigi.reply(message)

async def genshin_command(message: discord.Message):
    if "genshin" in message.content.lower():
        await message.add_reaction("💩")
        mess, image = rn.choice(RESPONSES), rn.choice(IMAGES)
        await message.reply(mess, file=discord.File(image))

async def cringe_command(message: discord.Message):
    if "!cringe" in message.content.lower():
        mess, image = rn.choice(RESPONSES), rn.choice(IMAGES)
        await message.channel.send(mess, file=discord.File(image))
    
async def help_command(message: discord.Message):
    if "!rbhelp" in message.content.lower():
        await message.reply(help.help_string)
            
async def add_react_command(message: discord.Message):
    if message.content.lower().startswith("!addreact"):
        await reactions.add_reaction(message)

async def reactlist_command(message: discord.Message):
    if "!reactlist" in message.content.lower():
        await reactions.list_reacts(message)

async def react_command(message: discord.Message):
    if "!react" in message.content.lower():
        await reactions.reply_with_reaction(message)

async def dn_command(message: discord.Message):
    if "deez nuts" in message.content.lower():
        await message.reply("AHA, GOTEEM", file=discord.File("images/goteem.jpg"))

async def playlist_command(message: discord.Message):
    if message.content.startswith("!playlist"):
        if len(message.content.split(' ')) == 1:
            await message.reply(content='Error: URL argument not supplied.')
        else:
            status, response, playlist = playlist_save.export(message.content.split(' ')[1])
            if status != 0:
                await message.reply(content=response)
            else:
                embed=discord.Embed(title=response, description=message.content.split(' ')[1])
                i=0
                for video in playlist['videos']:
                    embed.add_field(name=video['title'], value=video['url'], inline=True)
                    i += 1
                    if i > 26: break
                if len(playlist['videos']) > 25:
                    length = len(playlist['videos'])-25
                    embed.set_footer(text=f'{length} more...')
                await message.reply(embed=embed, file=discord.File('output.json'))