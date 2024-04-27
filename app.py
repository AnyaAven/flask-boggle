from flask import Flask, request, render_template, jsonify
from uuid import uuid4
from flask_debugtoolbar import DebugToolbarExtension


from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game_id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.jinja")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()

    # Set the new game into our games database
    games["game_id"] = game

    # Data to be jsonified
    game_id_and_board = {
        "gameId": game_id,
        "board": game.board
    }

    return jsonify(game_id_and_board)


@app.post("/api/score-word")
def score_word():
    """ Check if word is legal,
    in the word list,
    and is findable on the board

    if not a word return: {result: "not-word"}

    if not on board return: {result: "not-on-board"}

    if a valid word return: {result: "ok"}
    """

    game_data = request.json  # { gameId: "example-game-id", word: "example"}

    word = game_data["word"]
    game_id = game_data["gameId"]
    game = games[game_id]

    if not game.is_word_in_word_list(word):
        return jsonify({"result": "not-word"})

    elif game.check_word_on_board(word):
        return jsonify({"result": "ok"})

    else:
        return jsonify({"result": "not-on-board"})

