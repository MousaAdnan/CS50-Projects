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

                if (data.winner) {
                    setTimeout(() => {
                        alert(data.winner === "Tie" ? "It's a tie!" : `${data.winner} wins!`);
                    }, 100);
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
});
