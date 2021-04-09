import asyncio
import discord
import json
import random

def get_images():
    file = open("mario_images.json")
    return json.load(file)

mario_images = get_images() # imported from a json

async def reply(message: discord.message.Message):
    image = random.choice(mario_images)
    await message.reply("", file=discord.File(f'mario/{image}'))