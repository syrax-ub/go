#https://github.com/sanjit-sinha/rocklinks-bypaas

import time
import cloudscraper
from bs4 import BeautifulSoup 
from telegram import*
from telegram.ext import*
from os import getenv

TOKEN= getenv("TOKEN", None)
 
updater = Updater(TOKEN)
dispatcher = updater.dispatcher


def rocklinks_bypass(update ,context):
    message = update.effective_message
    args= context.args
    url = " ".join(args)
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://links.spidermods.in"
    else:
        DOMAIN = "https://rocklink.in"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: 
      inputs = soup.find(id="go-link").find_all(name="input")
    except: 
        return #"Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        joke= r.json()['url']
        bot.send_message(message.chat.id, joke) 
    except Exception as e:
        bot.send_message(message.chat.id, str(e))
        return  
    
dispatcher.add_handler(CommandHandler("link", rocklinks_bypass))
updater.start_polling()
