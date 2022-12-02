from flask import Flask, request
import telepot
import json

app = Flask(__name__)

with open('configs/env.json','r') as f:
    cfg = json.load(f)

token = cfg['TOKEN']
secret = cfg['SECRET']

bot = telepot.Bot(token)
bot.setWebhook("https://f4q73p.deta.dev/{}".format(secret), max_connections=1)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id, "From the web: you said '{}'".format(text))
    return "OK"