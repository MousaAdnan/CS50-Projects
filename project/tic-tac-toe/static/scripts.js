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
        const message = winner === "Tie" ? "It's a tie!" : `${winner} wins!`;
        $("#winner").text(message);
    }
});
