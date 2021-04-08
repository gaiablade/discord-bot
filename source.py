import discord
import random
import json
import ctypes
import pathlib
import re
import logging
import json

logging.basicConfig(filename="log.txt", level=logging.INFO)

REGEX = r"(?i)\b((?:https?://|\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

responses = [
    "cringe",
    "oh brother this STINKS",
    "damn bro, that's kinda cringe",
    "ratio",
    "no <3",
    "user has been banned for 3 hours for posting cringe",
    "cringe detected, deploying tear gas"
]

images = [
    "bottle_cat.jpg",
    "new_jersey.jpg"
]

mario_images = [] # imported from a json
with open("mario_images.json") as file:
    mario_images = json.load(file)

print(random.choice(responses) + " " + random.choice(images))

path = pathlib.Path().absolute() / "libroll.so"
libRoll = ctypes.CDLL(path)

token = None
with open("token.json") as json_file:
    data = json.load(json_file)
    token = data["token"]

print('initializing client')
client = None
try:
    client = discord.Client()
except:
    print('exception')

def roll(n: int):
    r = libRoll.roll(n)
    return r

@client.event
async def on_ready():
    print("Ready!")

@client.event
async def on_message(message):
    print(message.author.name)
    logging.info(f'Message from {message.author.name}: {message.content}')
    to_chastize = "Willybold_Plack"
    #to_chastize = "gaia_blade"
    if message.author.name == to_chastize:
        await message.add_reaction("💩")
        print('here')
        if message.attachments or re.search(REGEX, message.content):
            mess, image = random.choice(responses), random.choice(images)
            print(f'{mess} {image}')
            await message.reply(mess, file=discord.File(image))

    if message.content.startswith("!rolld"):
        r = re.search("^!rolld(\w+).*$", message.content)
        try:
            n = int(r[1])
            await message.channel.send("{0}!".format(roll(n)))
        except ValueError:
            await message.channel.send("Failed to parse")

    if "among" in message.content.lower() or "amogus" in message.content.lower():
        await message.reply("WHEN THE IMPOSTER IS SUS", file=discord.File("amongsomebitches.jpg"))

    if "loss" in message.content.lower():
        await message.reply("| || || |_", file=discord.File("loss.jpg"))

    if message.content == "!mario":
        image = random.choice(mario_images)
        print(f'mario image: {image}')
        await message.reply("", file=discord.File(f'mario/{image}'))


"""
@client.event
async def on_error(event, *args, **kwargs):
    print('error')
"""

@client.event
async def on_connect():
    print('connected')

client.run(token)