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
    r = re.search("!roll((\d+)?d(\d+)(\s*[+-]\s*\d+)*)", message.content)
    nat1 = False
    if r:
        n = int(r[2]) if r[2] else 1
        m = int(r[3]) if r[3] else 20
        fstring = r[1] if r[1] else 'undefined'
        all_rolls = []

        offset = 0
        offsets = re.findall('\s*([+-])\s*(\d+)', message.content)
        for o in offsets:
            offset += (int(o[1])) if o[0] == '+' else (-int(o[1]))
        
        sum = 0
        for i in range(n):
            rl = roll(m)
            if rl == 1: nat1 = True
            sum += rl
            all_rolls.append(str(rl))
        
        sum += offset
        
        all_rolls_str = [val + ' ' for val in all_rolls]
        all_rolls_str = ''.join(all_rolls_str)
        
        mess  = '```Markdown\n'
        mess += f'# {sum}\n'
        mess += f'Details:[{fstring} ( {all_rolls_str})]'
        mess += f'```'

        await message.channel.send(mess)
    else:
        await message.channel.send('Failed to parse.')

    return nat1