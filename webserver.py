from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "Hello World!"

def run():
  app.run(host="0.0.0.0", port=8000)

def start():
  server = Thread(target=run)
  server.start()
