from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "secret_key"  # Needed for session management


# Initialize the game state
def initialize_game():
    session["board"] = [""] * 9  # Empty 3x3 board
    session["turn"] = "X"        # Player starts
    session["winner"] = None
    if "scores" not in session:
        session["scores"] = {"player": 0, "computer": 0, "ties": 0}


@app.route("/")
def index():
    if "board" not in session:
        initialize_game()
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    position = data["position"]

    # Get the current game state
    board = session["board"]
    turn = session["turn"]

    # Ensure the move is valid
    if board[position] == "" and turn == "X":  # Player's move
        board[position] = "X"
        winner = check_winner(board)
        if winner:
            update_score(winner)
            session["board"] = board
            return jsonify({"winner": winner, "board": board, "scores": session["scores"]})

        # Computer's turn
        computer_move()
        winner = check_winner(session["board"])
        if winner:
            update_score(winner)
            return jsonify({"winner": winner, "board": session["board"], "scores": session["scores"]})

    # Update the game state
    session["board"] = board
    return jsonify({"board": board, "winner": None, "scores": session["scores"]})


@app.route("/reset", methods=["POST"])
def reset():
    initialize_game()
    return jsonify({"success": True})


# Determine the winner or check for a tie
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    # Check for a winner
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return board[combo[0]]  # Return "X" or "O"

    # Check for a tie
    if "" not in board:  # No empty spaces left
        return "Tie"

    return None


# Update the scores
def update_score(winner):
    scores = session["scores"]
    if winner == "X":  # Player wins
        scores["player"] += 1
    elif winner == "O":  # Computer wins
        scores["computer"] += 1
    elif winner == "Tie":  # Game is a tie
        scores["ties"] += 1
    session["scores"] = scores  # Save updated scores


# Handle the computer's move
def computer_move():
    board = session["board"]

    # Check if the computer can win
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner(board) == "O":
                session["board"] = board
                return
            board[i] = ""  # Undo the move

    # Check if the player is about to win, and block
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner(board) == "X":
                board[i] = "O"  # Block the player's win
                session["board"] = board
                return
            board[i] = ""  # Undo the move

    # Otherwise, choose a random empty position
    empty_positions = [i for i, value in enumerate(board) if value == ""]
    if empty_positions:
        position = random.choice(empty_positions)
        board[position] = "O"
        session["board"] = board


if __name__ == "__main__":
    app.run(debug=True)
