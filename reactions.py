import asyncio
import discord
import json
import random
import requests

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

def load():
    file = open("reactions.json")
    return json.load(file)

reaction_images = load()

async def add_reaction(message: discord.message.Message):
    words = message.content.split(' ')
    if len(message.attachments) > 0:
        file = message.attachments[0]
        if "image" in file.content_type:
            filename = f'reactions/{file.filename}'
            url = file.url
            if filename in reaction_images:
                await message.reply(f'{file.filename} already added!')
            else:
                print(f'Downloading {filename} from {url}')
                await download(url, filename)
                key = ''
                if len(words) > 1:
                    key = words[1]
                else:
                    key = file.filename
                reaction_images[key] = filename
                await message.reply(f'Added {key} to the available reactions!')
                with open("reactions.json", "w") as file:
                    json.dump(reaction_images, file)
        else:
            await message.reply(f'Attachment not an image type')
    else:
        await message.reply(f'No images attached!')
    
async def reply_with_reaction(message: discord.message.Message):
    words = message.content.split(' ')
    index = words.index('!react')
    print(f'{len(words)} {index+1}')
    print(reaction_images.keys())
    if len(words) <= index+1:
        filename = random.choice(list(reaction_images.keys()))
        await message.channel.send("", file=discord.File(reaction_images[filename]))
    else:
        if reaction_images[words[index+1]]:
            await message.channel.send("", file=discord.File(reaction_images[words[index+1]]))
        else:
            filename = random.choice(list(reaction_images.keys()))
            await message.channel.send("", file=discord.File(reaction_images[filename]))

async def list_reacts(message: discord.message.Message):
    words = message.content.split()
    reactions = list(reaction_images.keys())
    num_reactions = len(reactions)
    
    page = 1
    if len(words) >= words.index("!reactlist"):
        try:
            page = int(words[words.index('!reactlist') + 1])
        except:
            page = 1

    res = f'```\nPage {page} of {int(num_reactions / 10 + 1)}\n'
    for i in range(10):
        if i * page < num_reactions:
            res += f'{i+1}. {reactions[i * page]}\n'
        
    res += '```'
    await message.reply(res)

