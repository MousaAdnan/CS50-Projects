from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

game_state = {
    "board": [""] * 9,
    "turn": "X",
    "winner": None,
    "scores": {"player": 0, "computer": 0, "ties": 0},
}

def initialize_game():
    game_state["board"] = [""] * 9
    game_state["turn"] = "X"
    game_state["winner"] = None
    game_state["scores"] = {"player": 0, "computer": 0, "ties": 0}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    position = data["position"]


    board = game_state["board"]
    turn = game_state["turn"]


    if board[position] == "" and turn == "X":
        board[position] = "X"
        winner = check_winner(board)
        if winner:
            update_score(winner)
            return jsonify({"winner": winner, "board": board, "scores": game_state["scores"]})

        computer_move()
        winner = check_winner(board)
        if winner:
            update_score(winner)
            return jsonify({"winner": winner, "board": board, "scores": game_state["scores"]})

    return jsonify({"board": board, "winner": None, "scores": game_state["scores"]})


@app.route("/reset", methods=["POST"])
def reset():
    game_state["board"] = [""] * 9
    game_state["turn"] = "X"
    game_state["winner"] = None
    return jsonify({"success": True})


def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]              
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]]

    if "" not in board:
        return "Tie"

    return None


def update_score(winner):
    if winner == "X":
        game_state["scores"]["player"] += 1
    elif winner == "O":
        game_state["scores"]["computer"] += 1
    elif winner == "Tie":
        game_state["scores"]["ties"] += 1


def computer_move():
    board = game_state["board"]

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner(board) == "O":
                return
            board[i] = ""

    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner(board) == "X":
                board[i] = "O"
                return
            board[i] = ""

    empty_positions = [i for i, value in enumerate(board) if value == ""]
    if empty_positions:
        position = random.choice(empty_positions)
        board[position] = "O"


if __name__ == "__main__":
    app.run(debug=True)
