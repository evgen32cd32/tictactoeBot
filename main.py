from flask import Flask, request, render_template
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import json
import ttt_game as game
import uuid

app = Flask(__name__)

with open('configs/env.json','r') as f:
    cfg = json.load(f)

token = cfg['TOKEN']
secret = cfg['SECRET']
domain = cfg['DOMAIN']

bot = telepot.Bot(token)
bot.setWebhook("{}/{}".format(domain,secret), max_connections=1)

try:
    (start,botG) = game.load_game()
except Exception:
    print("Can't load. New initialization")
    start = game.init_states()
    botG = game.Bot(start,expl_rate=0.5)

gamesDict = {}

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/action', methods={"POST"})
def player_action():
    d = request.get_json()
    resp = {}
    if 'start' in d or d['gameId'] not in gamesDict:
        gid = str(uuid.uuid4())
        gamesDict[gid] = start
        resp['field'] = start.s
        resp['gameId'] = gid
        resp['end'] = False
        return resp
    d['end'] = False
    for child in gamesDict[d['gameId']].children:
        if child.s == d['field']:
            if child.winner is None:
                ns = botG.action(child)
                gamesDict[d['gameId']] = ns
                if ns.winner is not None:
                    d['end'] = True
                    del gamesDict[d['gameId']]
                d['field'] = ns.s
            else:
                d['end'] = True
                del gamesDict[d['gameId']]
            return d
    d['field'] = gamesDict[d['gameId']].s
    return d

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id, "From the web: you said '{}'".format(text),reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text='Yes'),KeyboardButton(text='No')],
            [KeyboardButton(text='Left'),KeyboardButton(text='Right')]]))
    return "OK"


if __name__ == '__main__':
   app.run(debug=True)