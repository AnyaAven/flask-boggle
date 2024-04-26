from flask import Flask, request, render_template, jsonify
from uuid import uuid4
from flask_debugtoolbar import DebugToolbarExtension


from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
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
    games["gameId"] = game_id
    games["board"] = game.board

    json_data = jsonify(games)
    breakpoint()

    return jsonify(games)
