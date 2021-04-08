import json
import urllib.request
import asyncio
import requests
import re

j = None
with open('output1.json') as file:
    j = json.load(file)

async def download(url, n):
    extension_reg = ".*\.(.*)"
    extension = re.match(extension_reg, url)
    with open(f'mario/{n}.{extension[1]}', 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            return
        
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

async def main():
    n = 0
    for file in j:
        await download(file, n)
        n += 1

if __name__ == "__main__":
    asyncio.run(main())