from flask import Flask, request, render_template
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import json
from ttt_game import TTTGame
import uuid
import random
import os
from secrets import token_urlsafe

app = Flask(__name__)

token = f"{os.getenv('BOT_TOKEN')}"
secret = token_urlsafe()
domain = f"https://{os.getenv('DETA_SPACE_APP_HOSTNAME')}/"

bot = None

game = TTTGame()

gamesDict = {}

expl_rate = {
    "Easy":0.25,
    "Medium":0.5,
    "Hard":0.75,
    "Impossible":1.0
}

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/action', methods={"POST"})
def player_action():
    d = request.get_json()
    resp = {}
    print(f'IN: {d}')
    # New Game
    if 'start' in d or d['gameId'] not in gamesDict:
        if 'gameId' in d:
            gid = d['gameId']
        else:
            gid = str(uuid.uuid4())
        if d['player'] == 'Random':
            if random.randint(0, 1) == 1:
                d['player'] = 'First player'
            else:
                d['player'] = 'Second player'
        if d['player'] == 'First player':
            gamesDict[gid] = game.startState()
            resp['field'] = gamesDict[gid].s
        else:
            ns, tr = game.bot.action(game.startState(),expl_rate=expl_rate[d['lvl']])
            gamesDict[gid] = ns
            resp['field'] = TTTGame.fromSpiral(ns.getTransformed(tr))
        resp['gameId'] = gid
        resp['status'] = 'player_move'
        print(f'OUT: {resp}')
        return resp
    
    # Get new state
    ca, trans = game.checkCorrectMove(TTTGame.toSpiral(d['field']),gamesDict[d['gameId']])

    # Cheater
    if ca is None:
        resp['field'] = gamesDict[d['gameId']].s
        resp['gameId'] = d['gameId']
        resp['status'] = 'cheater'
        print(f'OUT: {resp}')
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
        print(f'OUT: {resp}')
        return resp

    # Bot move
    ns, tr = game.bot.action(ca,gamesDict[d['gameId']],expl_rate=expl_rate[d['lvl']])
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
        print(f'OUT: {resp}')
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