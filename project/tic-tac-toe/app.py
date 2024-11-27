from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "secret"  # Needed to use Flask sessions

# Initialize the board and scores
def initialize_game():
    session["board"] = [""] * 9
    session["scores"] = {"player1": 0, "player2": 0, "ties": 0}
    session["turn"] = "X"  # X always starts

@app.route("/")
def index():
    if "board" not in session:
        initialize_game()
    return render_template("index.html", scores=session["scores"])

@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    position = data["position"]
    mode = data["mode"]

    board = session.get("board", [""] * 9)  # Ensure the board is retrieved
    turn = session.get("turn", "X")  # Default turn starts with X

    # Check if the position is valid
    if board[position] == "":
        if mode == "computer":
            # User always places X
            board[position] = "X"
            winner = check_winner(board)
            if winner:
                update_score("X")
                session["board"] = board  # Persist the updated board
                return jsonify({"winner": "Player 1", "board": board})

            # Computer's turn as "O"
            computer_move()
            winner = check_winner(board)
            if winner:
                update_score("O")
                session["board"] = board  # Persist the updated board
                return jsonify({"winner": "Computer", "board": board})

        else:
            # For Player vs Player mode
            board[position] = turn  # Place the current player's move
            winner = check_winner(board)
            if winner:
                update_score(turn)
                session["board"] = board  # Persist the updated board
                winner_name = "Player 1" if turn == "X" else "Player 2"
                return jsonify({"winner": winner_name, "board": board})
            session["turn"] = "O" if turn == "X" else "X"  # Switch turn

    # Persist the updated board and return it
    session["board"] = board
    return jsonify({"board": board, "winner": None})




@app.route("/reset", methods=["POST"])
def reset():
    initialize_game()
    return jsonify({"success": True})

# Update scores
def update_score(winner):
    scores = session.get("scores", {"player1": 0, "player2": 0, "ties": 0})

    if winner == "X":  # Player 1 wins
        scores["player1"] += 1
    elif winner == "O":  # Player 2 or Computer wins
        scores["player2"] += 1
    elif winner == "Tie":  # It's a tie
        scores["ties"] += 1

    session["scores"] = scores  # Save the updated scores


# Check if there's a winner or a tie
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

    return None  # No winner or tie yet


def computer_move():
    board = session["board"]

    # Check if the computer can win
    for i in range(9):
        if board[i] == "":  # Ensure the position is empty
            board[i] = "O"  # Temporarily make a move
            if check_winner(board) == "O":  # Check if this move wins
                return  # Keep this move if it leads to a win
            board[i] = ""  # Undo the move

    # Check if the player is about to win, and block
    for i in range(9):
        if board[i] == "":  # Ensure the position is empty
            board[i] = "X"  # Temporarily block the player's move
            if check_winner(board) == "X":  # Check if this move blocks
                board[i] = "O"  # Block the player's win
                return  # End the computer's turn
            board[i] = ""  # Undo the move

    # Otherwise, choose a random empty position
    empty_positions = [i for i, value in enumerate(board) if value == ""]
    if empty_positions:
        position = random.choice(empty_positions)
        board[position] = "O"  # Make the move in a valid empty position



if __name__ == "__main__":
    app.run(debug=True)
