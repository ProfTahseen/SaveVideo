from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():

    message = '''I am alive! My Invite Link: https://discord.com/api/oauth2/authorize?client_id=783728124021702689&permissions=191488&scope=bot'''

    return message

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()