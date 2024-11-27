from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Global state
game_state = {
    "board": [""] * 9,
    "turn": "X",
    "winner": None,
    "scores": {"player": 0, "computer": 0, "ties": 0},
}


# Initialize the game state
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

    # Get the current game state
    board = game_state["board"]
    turn = game_state["turn"]

    # Ensure the move is valid
    if board[position] == "" and turn == "X":  # Player's move
        board[position] = "X"
        winner = check_winner(board)
        if winner:
            update_score(winner)
            return jsonify({"winner": winner, "board": board, "scores": game_state["scores"]})

        # Computer's turn
        computer_move()
        winner = check_winner(board)
        if winner:
            update_score(winner)
            return jsonify({"winner": winner, "board": board, "scores": game_state["scores"]})

    # Update the game state
    return jsonify({"board": board, "winner": None, "scores": game_state["scores"]})


@app.route("/reset", methods=["POST"])
def reset():
    # Reset only the board and turn
    game_state["board"] = [""] * 9
    game_state["turn"] = "X"
    game_state["winner"] = None
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
    if winner == "X":  # Player wins
        game_state["scores"]["player"] += 1
    elif winner == "O":  # Computer wins
        game_state["scores"]["computer"] += 1
    elif winner == "Tie":  # Game is a tie
        game_state["scores"]["ties"] += 1


# Handle the computer's move
def computer_move():
    board = game_state["board"]

    # Check if the computer can win
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner(board) == "O":
                return
            board[i] = ""  # Undo the move

    # Check if the player is about to win, and block
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner(board) == "X":
                board[i] = "O"  # Block the player's win
                return
            board[i] = ""  # Undo the move

    # Otherwise, choose a random empty position
    empty_positions = [i for i, value in enumerate(board) if value == ""]
    if empty_positions:
        position = random.choice(empty_positions)
        board[position] = "O"


if __name__ == "__main__":
    app.run(debug=True)
