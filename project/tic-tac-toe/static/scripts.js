let mode = "player"; // Default mode: Player vs Player

$(document).ready(function () {
    // Handle cell clicks
    $(".cell").click(function () {
        const position = $(this).data("position");

        $.ajax({
            url: "/move",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ position: position, mode: mode }),
            success: function (data) {
                updateBoard(data.board);

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

    // Switch to playing against the computer
    $("#play-computer").click(function () {
        mode = "computer";
        resetGame();
        alert("Playing against Computer!");
    });

    // Switch to Player vs Player
    $("#play-player").click(function () {
        mode = "player";
        resetGame();
        alert("Playing against another Player!");
    });
});

// Update the board in the frontend
function updateBoard(board) {
    $(".cell").each(function (index) {
        $(this).text(board[index]); // Update each cell with X, O, or empty
    });
}

// Reset the game
function resetGame() {
    $.ajax({
        url: "/reset",
        type: "POST",
        success: function () {
            $(".cell").text(""); // Clear the board
        },
        error: function () {
            alert("An error occurred while resetting the game.");
        },
    });
}
