$(document).ready(function () {
    let mode = "player"; // Default mode: Player vs Player

    // Handle cell clicks
    $(".cell").click(function () {
        const position = $(this).data("position");

        $.ajax({
            url: "/move",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ position: position, mode: mode }),
            success: function (data) {
                updateBoard(data.board); // Update the board

                if (data.winner) {
                    setTimeout(() => {
                        alert(data.winner === "Tie" ? "It's a tie!" : `${data.winner} wins!`);
                        refreshScores(); // Update scores dynamically
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

    // Function to fetch and update scores
    function refreshScores() {
        $.ajax({
            url: "/scores",
            type: "GET",
            success: function (data) {
                $("#player1").text(data.player1); // Update Player 1 score
                $("#player2").text(data.player2); // Update Player 2/Computer score
                $("#ties").text(data.ties);       // Update ties
            },
            error: function () {
                alert("An error occurred while updating the scores.");
            },
        });
    }

    // Call refreshScores on page load to ensure scores are accurate
    refreshScores();

    // Update the entire board in the frontend
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
                refreshScores(); // Refresh scores
            },
            error: function () {
                alert("An error occurred while resetting the game.");
            },
        });
    }
});
