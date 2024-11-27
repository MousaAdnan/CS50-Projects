from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "secret"  # Needed to use Flask sessions

# Initialize the board and scores
def initialize_game():
    session["board"] = [""] * 9
    session["turn"] = "X"  # X always starts

@app.route("/")
def index():
    if "board" not in session:
        initialize_game()
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    position = data["position"]

    board = session.get("board", [""] * 9)
    turn = session.get("turn", "X")

    # Check if the position is valid
    if board[position] == "":
        board[position] = turn  # Place the current player's move
        winner = check_winner(board)
        if winner:
            session["board"] = board  # Persist the updated board
            return jsonify({"winner": winner, "board": board})

        # Switch turn
        session["turn"] = "O" if turn == "X" else "X"

        # If it's the computer's turn, let it make a move
        if session["turn"] == "O":
            computer_move()
            winner = check_winner(session["board"])
            if winner:
                return jsonify({"winner": winner, "board": session["board"]})

    # Persist the updated board and return it
    session["board"] = board
    return jsonify({"board": board, "winner": None})

@app.route("/reset", methods=["POST"])
def reset():
    initialize_game()
    return jsonify({"success": True})

# Check if there's a winner
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    # Check for a winner
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]]  # Return "X" or "O" (the winner)

    # Check for a tie
    if "" not in board:  # No empty spaces and no winner
        return "Tie"

    return None  # No winner yet

# Computer makes a move
def computer_move():
    board = session["board"]

    # Randomly choose an empty position
    empty_positions = [i for i, value in enumerate(board) if value == ""]
    if empty_positions:
        position = random.choice(empty_positions)
        board[position] = "O"  # Computer plays as "O"

if __name__ == "__main__":
    app.run(debug=True)
