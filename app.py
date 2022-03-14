from flask import Flask, render_template, request, jsonify
import os, sys
path = '/game'
sys.path.append(os.path.join(os.getcwd(), 'game'))

from game.game_state import GameState



app = Flask(__name__)
app.templates_auto_reload = True

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/game",  methods=['GET', 'POST'])
def start_game():
    # ! check if valid FEN
    FEN = request.form.get('FEN')
    print(FEN)
    if FEN == '':
        game_state = GameState()
    else:
        game_state = GameState(FEN)
    position = str(game_state)
    print(position)
    return render_template("game.html", board_pos = position.split())