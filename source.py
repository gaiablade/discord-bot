import discord
import random as rn
import json
import ctypes
import pathlib
import re
import json
import logging
import urllib.request
import requests

import help
import luigi
import mario
import reactions
import roll

REGEX = r"(?i)\b((?:https?://|\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

logging.basicConfig(filename="logging.txt", level=logging.DEBUG)

# Log to file and console:
def log(str):
    with open("log.txt", "a") as file:
        file.write(str)
    print(str)

# Download image
async def download(url, filename):
    with open(filename, 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            return
        
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

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

AMONGUS_IMAGES = [
    "images/amongsomebitches.jpg",
    "images/impostersus.jpg"
]

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

# EVENTS:

@client.event
async def on_ready():
    print("Bot connected")

@client.event
async def on_message(message: discord.message.Message):
    try:
        if "dice-roll" not in message.author.display_name:
            log(f'-New Message-')
            log(f'Content: {message.content}')
            log(f'Display Name: {message.author.display_name}')

            # Roll dice (dice parser replacement)
            if message.content.startswith("!roll"):
                nat1 = await roll.roll_dice(message, str(message.content))
                if nat1:
                    mess, image = rn.choice(RESPONSES), rn.choice(IMAGES)
                    await message.channel.send(mess, file=discord.File(image))

            elif "among" in message.content.lower() or "amogus" in message.content.lower() or "sus" in message.content.lower() or "imposter" in message.content.lower():
                image = rn.choice(AMONGUS_IMAGES)
                await message.reply("WHEN THE IMPOSTER IS SUS", file=discord.File(image))

            elif "loss" in message.content.lower():
                await message.reply("| l| || |_", file=discord.File("images/loss.jpg"))

            elif "!mario" in message.content.lower():
                await mario.reply(message)

            elif "!luigi" in message.content.lower():
                await luigi.reply(message)

            elif "genshin" in message.content.lower():
                await message.add_reaction("💩")
                mess, image = rn.choice(RESPONSES), rn.choice(IMAGES)
                await message.reply(mess, file=discord.File(image))

            elif "!cringe" in message.content.lower():
                mess, image = rn.choice(RESPONSES), rn.choice(IMAGES)
                await message.channel.send(mess, file=discord.File(image))

            elif "!rbhelp" in message.content.lower():
                await message.reply(help.help_string)
            
            elif message.content.lower().startswith("!addreact"):
                await reactions.add_reaction(message)
            
            elif "!reactlist" in message.content.lower():
                await reactions.list_reacts(message)
            
            elif "!react" in message.content.lower():
                await reactions.reply_with_reaction(message)

    except Exception as e:
        print('Exception occured')
        print(e)

"""
@client.event
async def on_error(event, *args, **kwargs):
    print('error')
"""

@client.event
async def on_connect():
    pass

client.run(token)