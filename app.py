from flask import Flask, render_template, request
import os, sys

path = '/game'
sys.path.append(os.path.join(os.getcwd(), 'game'))
import game.tryimport as tryimport
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    tryimport.main()
    return render_template("index.html")

@app.route("/game",  methods=['GET', 'POST'])
def start_game():
    FEN = request.form.get('FEN')
    if FEN == '':
        FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    return render_template("game.html", board_pos = FEN)