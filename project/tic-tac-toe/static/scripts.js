$(document).ready(function () {
    // Handle cell clicks
    $(".cell").click(function () {
        const position = $(this).data("position");

        $.ajax({
            url: "/move",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ position: position }),
            success: function (data) {
                updateBoard(data.board); // Update the board

                if (data.winner) {
                    setTimeout(() => {
                        alert(data.winner === "Tie" ? "It's a tie!" : `${data.winner} wins!`);
                        resetGame();
                    }, 100);
                }
            },
            error: function () {
                alert("An error occurred while making a move.");
            },
        });
    });

    // Reset the game
    $("#reset").click(function () {
        resetGame();
    });

    // Update the entire board
    function updateBoard(board) {
        $(".cell").each(function (index) {
            $(this).text(board[index]); // Update each cell with the current board state
        });
    }

    // Reset the game and clear the board
    function resetGame() {
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
    }
});
