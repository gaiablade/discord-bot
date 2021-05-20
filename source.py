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

import bot_commands as bot

import help
import reactions
from youtube import playlist_save

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

# Open bot token
token = json.load(open('token.json'))['token']

client = None
try:
    client = discord.Client()
except:
    log("Failed to initialize client")

# EVENTS:

@client.event
async def on_ready():
    print("Bot ready...")

@client.event
async def on_message(message: discord.message.Message):
    try:
        if "dice-roll" not in message.author.display_name:
            log(f'-New Message-\n')
            log(f'Content: {message.content}\n')
            log(f'Display Name: {message.author.display_name}\n')
            log(f'--------------------------------------------------------\n')

            commands = [bot.dice_roll_command, bot.amogus_command, bot.loss_command, bot.mario_command, bot.luigi_command,
                        bot.genshin_command, bot.cringe_command, bot.help_command, bot.add_react_command,
                        bot.reactlist_command, bot.react_command, bot.dn_command, bot.playlist_command]

            for command in commands:
                done = await command(message)
                if done: break

    except Exception as e:
        log(f'Exception occured\n')
        log(f'{e}\n')
        log(f'\n')

@client.event
async def on_connect():
    print("Connected to Discord...")

client.run(token)