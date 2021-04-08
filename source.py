import discord
import random
import json
import ctypes
import pathlib
import re
import json
import logging

REGEX = r"(?i)\b((?:https?://|\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

logging.basicConfig(filename="logging.txt", level=logging.DEBUG)

# Log to file and console:
def log(str):
    with open("log.txt", "a") as file:
        file.write(str)
    print(str)

help_string = '''
```
roll-bot commands:

!rolld[n] -> Roll an n-sided dice.

!mario -> Fun Mario picture.

------------------------------------
Event words:
among, amogus, loss
```
'''

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
    "images/new_jersey.jpg"
]

mario_images = None # imported from a json
with open("mario_images.json") as file:
    mario_images = json.load(file)

# Load C++ library
path = pathlib.Path().absolute() / "libroll.so"
libRoll = ctypes.CDLL(path)

# Open bot token
token = None
with open("token.json") as json_file:
    data = json.load(json_file)
    token = data["token"]

client = None
try:
    client = discord.Client()
except:
    log("Failed to initialize client")

def roll(n: int):
    r = libRoll.roll(n)
    return r




# EVENTS:



@client.event
async def on_ready():
    print("Bot connected")

@client.event
async def on_message(message):
    if "dice-roll" not in message.author.display_name:
        log(f'-New Message-')
        log(f'Content: {message.content}')
        log(f'Display Name: {message.author.display_name})')
        to_chastize = "Willybold_Plack"
        #to_chastize = "gaia_blade"
        if message.author.display_name == to_chastize:
            try:
                await message.add_reaction("💩")
                if message.attachments or re.search(REGEX, message.content):
                    mess, image = random.choice(RESPONSES), random.choice(IMAGES)
                    await message.reply(mess, file=discord.File(image))
            except:
                pass

        if message.content.startswith("!rolld"):
            r = re.search("^!rolld(\w+).*$", message.content)
            try:
                n = int(r[1])
                await message.channel.send("{0}!".format(roll(n)))
            except ValueError:
                await message.channel.send("Failed to parse")
            except:
                pass

        elif "among" in message.content.lower() or "amogus" in message.content.lower():
            try:
                await message.reply("WHEN THE IMPOSTER IS SUS", file=discord.File("images/amongsomebitches.jpg"))
            except:
                pass

        elif "loss" in message.content.lower():
            try:
                await message.reply("| || || |_", file=discord.File("images/loss.jpg"))
            except:
                pass

        elif "!mario" in message.content.lower():
            try:
                if message.author.display_name == to_chastize:
                    await message.reply("", file=discord.File('images/amongsomebitches.jpg'))
                else:
                    image = random.choice(mario_images)
                    log(f'-Sending Reply-')
                    log(f'Image file: mario/{image}')
                    await message.reply("", file=discord.File(f'mario/{image}'))
            except:
                pass
        
        elif "genshin" in message.content.lower():
            try:
                await message.add_reaction("💩")
                mess, image = random.choice(RESPONSES), random.choice(IMAGES)
                await message.reply(mess, file=discord.File(image))
            except:
                pass

        
        elif "!rbhelp" in message.content.lower():
            try:
                await message.reply(help_string)
            except:
                pass


"""
@client.event
async def on_error(event, *args, **kwargs):
    print('error')
"""

@client.event
async def on_connect():
    pass

client.run(token)