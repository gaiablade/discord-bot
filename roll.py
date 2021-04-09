import asyncio
import ctypes
import discord
import pathlib
import re

path = pathlib.Path().absolute() / "libroll.so"
libRoll = ctypes.CDLL(path)

def roll(n: int):
    r = libRoll.roll(n)
    return r

# Load C++ library

async def roll_dice(message: discord.message.Message, parse_string: str):
    r = re.search("^!roll(\d+)?d(\w+).*$", message.content)
    if r:
        all_rolls = []
        m = int(r[1]) if r[1] else 1
        n = int(r[2])
        sum = 0
        for i in range(m):
            rl = roll(n)
            sum += rl
            all_rolls.append(rl)
        mess = '```\n'
        mess += f'{str(sum)}\n'
        for rl in all_rolls:
            mess += str(rl)
            mess += ' '
        mess += '\n```'
        await message.channel.send(mess)
    else:
        await message.channel.send("Failed to parse")