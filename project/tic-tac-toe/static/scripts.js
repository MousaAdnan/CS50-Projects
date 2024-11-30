$(document).ready(function () {
    let scores = { player: 0, computer: 0, ties: 0 };

    $(".cell").click(function () {
        const position = $(this).data("position");

        $.ajax({
            url: "/move",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ position: position }),
            success: function (data) {
                updateBoard(data.board);

                if (data.winner) {
                    updateScores(data.winner);
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
                $(".cell").text("");
                clearWinnerMessage();
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

    function updateScores(winner) {
        if (winner === "X") {
            scores.player += 1;
        } else if (winner === "O") {
            scores.computer += 1;
        } else if (winner === "Tie") {
            scores.ties += 1;
        }
        renderScores();
    }

    function renderScores() {
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
        $("#winner-message").text(""); 
    }
});
