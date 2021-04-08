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