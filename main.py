from flask import Flask, request, render_template
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import json

app = Flask(__name__)

with open('configs/env.json','r') as f:
    cfg = json.load(f)

token = cfg['TOKEN']
secret = cfg['SECRET']

#bot = telepot.Bot(token)
#bot.setWebhook("https://f4q73p.deta.dev/{}".format(secret), max_connections=1)

@app.route('/')
def home():
   return render_template('index.html',grid = [['X','O'],['Y'],['N']])

@app.route('/action', methods={"POST"})
def player_action():
    print(request.form)
    return "OK"

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        #bot.sendMessage(chat_id, "From the web: you said '{}'".format(text),reply_markup=ReplyKeyboardMarkup(
        #    keyboard=[[KeyboardButton(text='Yes'),KeyboardButton(text='No')],
        #    [KeyboardButton(text='Left'),KeyboardButton(text='Right')]]))
    return "OK"


if __name__ == '__main__':
   app.run(debug=True)