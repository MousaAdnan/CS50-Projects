$(document).ready(function () {
    $(".cell").click(function () {
        const position = $(this).data("position");

        $.ajax({
            url: "/move",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ position: position }),
            success: function (data) {
                updateBoard(data.board);
                updateScores(data.scores);

                if (data.winner) {
                    displayWinner(data.winner);
                }
            },
            error: function () {
                alert("An error occurred while making a move.");
            },
        });
    });

    $("#reset").click(function () {
        $.ajax({
            url: "/reset",
            type: "POST",
            success: function () {
                $(".cell").text(""); // Clear the board visually
                clearWinnerMessage(); // Clear the winner message
                // Do not modify the scoreboard
            },
            error: function () {
                alert("An error occurred while resetting the game.");
            },
        });
    });

    function updateBoard(board) {
        $(".cell").each(function (index) {
            $(this).text(board[index]);
        });
    }

    function updateScores(scores) {
        $("#player-wins").text(scores.player);
        $("#computer-wins").text(scores.computer);
        $("#ties").text(scores.ties);
    }

    function displayWinner(winner) {
        let message = "";
        if (winner === "X") {
            message = "Player 1 Wins!";
        } else if (winner === "O") {
            message = "Computer Wins!";
        } else if (winner === "Tie") {
            message = "Tie :(";
        }
        $("#winner-message").text(message);
    }

    function clearWinnerMessage() {
        $("#winner-message").text(""); // Clear the message
    }
});
