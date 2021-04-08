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

function download_file(url, filename) {
    request.head(url, function(err, res, body){
        console.log('content-type:', res.headers['content-type']);
        console.log('content-length:', res.headers['content-length']);
    
        request(url).pipe(fs.createWriteStream(filename)).on('close', () => {return true;});
    })
}

function get_extension_from_url(url) {
    let pattern = /.*\.(.*)/g
    const match = pattern.exec(url)
    if (match) {
        return match[1]
    } else {
        return ""
    }
}

async function download_luigis() {
    try {
        const luigi_page = "https://www.mariowiki.com/Gallery:Luigi_artwork_and_scans"
        let preview_urls = []
        let pat1 = /href="(\/File:[^"]*)"/g
        let html = await get_html(luigi_page)
        let found = pat1.exec(html)
        while (found != null) {
            preview_urls.push(`https://www.mariowiki.com${found[1]}`)
            found = pat1.exec(html)
        }
        console.log(preview_urls)

        let pat2 = /a href="(https:\/\/mario.wiki.gallery\/images\/[^"]*)"/g
        let image_urls = preview_urls.map(async(url) => {
            try {
                console.log(url)
                let new_html = await get_html(url)
                let found = pat2.exec(new_html)
                if (found) {
                    return found[1];
                } else {
                    return null
                }
            } catch (err) {
                return null
            }
        })
        Promise.all(image_urls).then((val) => {
            console.log(val)
            let n = 0
            for (let file of val) {
                if (file != null) {
                    let extension = get_extension_from_url(file)
                    download_file(file, `luigi/${n}.${extension}`)
                    n++
                }
            }
        }).catch((err) => {
            (() => {return true;})();
        })
    } catch (err) {
        console.error(err)
    }
}

download_luigis()