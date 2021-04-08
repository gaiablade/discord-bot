const https = require("https")
const fs = require("fs");
const request = require("request");

function get_html(file) {
    return new Promise((resolve, reject) => {
        request(`${file}`, (error, response, body) => {
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

async function get_html_async(file) {
    request(`${file}`, (error, response, body) => {
        if (error)  {
            throw new Error(error)
        }
        else if (response && response.statusCode != 200) {
            throw new Error("invalid status code")
        }
        else {
            return body
        }
    })

}

let arr = JSON.parse(fs.readFileSync("j.json"))

let urls = arr.map((file) => {
    return get_html(`https://www.mariowiki.com${file}`)
})

Promise.all(urls).then(value => {
    const pattern = /a href=\"(https:\/\/mario.wiki.gallery\/images\/[^\"]+)\"/
    let a = []

    console.log(`Length: ${value.length}`)

    for (let html of value) {
        let found = pattern.exec(html)
        if (found) {
            console.log(found[1])
            a.push(found[1])
        }
    }

    return a

}).then(value => {
    console.log(value)
    fs.writeFileSync("test.json", JSON.stringify(value, null, 2))
}).catch(err => {
    console.log("HERE")
    console.log(err)
    (() => {return true})();
})