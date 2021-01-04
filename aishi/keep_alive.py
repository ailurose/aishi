### This file will ensure that the bot stays active even when the
### repl.it tab is closed. Without this, the bot will be "off"
### whenever our repl.it server is off/tab is closed

### Note: Repl.it will still turn off server after 1 hr of inactivity
### We need to later set up something that will ping our bot to keep
### it alive later on

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is kept alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
