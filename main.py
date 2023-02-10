from flask import Flask, request, render_template
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import json
from ttt_game import TTTGame
import uuid

app = Flask(__name__)

with open('configs/env.json','r') as f:
    cfg = json.load(f)

token = cfg['TOKEN']
secret = cfg['SECRET']
domain = cfg['DOMAIN']

bot = None

game = TTTGame()

gamesDict = {}

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/action', methods={"POST"})
def player_action():
    d = request.get_json()
    resp = {}

    # New Game
    if 'start' in d or d['gameId'] not in gamesDict:
        gid = str(uuid.uuid4())
        gamesDict[gid] = game.startState()
        resp['field'] = gamesDict[gid].s
        resp['gameId'] = gid
        resp['status'] = 'player_move'
        return resp
    
    # Get new state
    print(d['field'])
    ca, trans = game.checkCorrectMove(TTTGame.toSpiral(d['field']),gamesDict[d['gameId']])

    # Cheater
    if ca is None:
        resp['field'] = gamesDict[d['gameId']].s
        resp['gameId'] = d['gameId']
        resp['status'] = 'cheater'
        return resp
    
    # Check GameOver
    if ca.winner is not None:
        resp['field'] = d['field']
        resp['gameId'] = d['gameId']
        if ca.winner == 'D':
            resp['status'] = 'draw'
        else:
            resp['status'] = 'player_won'
        game.bot.get_defeat(ca.winner,gamesDict[d['gameId']])
        del gamesDict[d['gameId']]
        return resp

    # Bot move
    ns, tr = game.bot.action(ca,gamesDict[d['gameId']])
    resp['field'] = TTTGame.fromSpiral(ns.getTransformed(trans + tr))
    resp['gameId'] = d['gameId']
    if ns.winner is None:
        resp['status'] = 'player_move'
        gamesDict[d['gameId']] = ns
    else:
        if ns.winner == 'D':
            resp['status'] = 'draw'
        else:
            resp['status'] = 'bot_won'
        del gamesDict[d['gameId']]
    return resp

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
else:
    bot = telepot.Bot(token)
    bot.setWebhook("{}/{}".format(domain,secret), max_connections=1)