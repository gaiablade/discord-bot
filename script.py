"""
const https = require("https")
const fs = require("fs");
const request = require("request")

function b(file) {
    //console.log(`https://www.mariowiki.com${file}`)
    return new Promise((resolve, reject) => {
        request(`https://www.mariowiki.com${file}`, (error, response, body) => {
            if (error)  {
                reject(error)
            }
            else if (response && response.statusCode != 200) {
                reject("invalid status code")
            }
            else {
                resolve(body)
            }
        })
    })
}

async function f() {
    console.log("Start")
    let arr = await JSON.parse(fs.readFileSync("j.json"))
    let shortened = [arr[0], arr[1], arr[2]]
    console.log(shortened)

    let urls = shortened.map(async (file) => {
        try {
            let a = await b(file)
            return a;
        } catch {
            return "e"
        }
    });
}

f();
"""
import http
import json
import urllib.request
import re

f = []

data = None
with open("j.json") as file:
    data = json.load(file)

for file in data:
    fp = urllib.request.urlopen(f'https://www.mariowiki.com{file}')
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    regex = r"a href=\"(https:\/\/mario.wiki.gallery\/images\/[^\"]+)\""

    x = re.search(regex, mystr)

    f.append(x[1])

with open("output.json", "w") as file:
    json.dump(f, file)
