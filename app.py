from flask import Flask, request, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "abc123"

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/', methods=["GET", "POST"])
def show_board():
 """Shows game board"""

 board = boggle_game.make_board()
 session['board'] = board
 highscore = session.get("highscore", 0)
 nplays = session.get("nplays", 0)

 return render_template("boggle-board.html", board=board, highscore=highscore, nplays=nplays)

@app.route('/check-guess', methods=[ "GET","POST"])
def check_guess():
 """Check if guessed word is valid"""

 word = request.args["word"]
 board = session['board']
 res = boggle_game.check_valid_word(board, word)

 return jsonify({'result': res})


@app.route('/post-score', methods=["GET","POST"])
def get_score():
 """posts score"""
 score = request.json["score"]
 highscore = session.get("highscore", 0)
 nplays = session.get("nplays", 0)

 session["nplays"] = nplays + 1
 session["highscore"] = max(score, highscore)
 return jsonify(brokeRecord=score > highscore)
 

