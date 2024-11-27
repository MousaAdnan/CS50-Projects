let mode = "player";

$(document).ready(function () {
    $(".cell").click(function () {
        let position = $(this).data("position");
        $.post("/move", JSON.stringify({ position: position, mode: mode }), function (data) {
            updateBoard(data.board);
            if (data.winner) {
                alert(data.winner === "Tie" ? "It's a tie!" : `${data.winner} wins!`);
            }
        }, "json");
    });

    $("#reset").click(function () {
        $.post("/reset", {}, function () {
            $(".cell").text("");
        }, "json");
    });

    $("#play-computer").click(function () {
        mode = "computer";
        alert("Playing against Computer!");
    });

    $("#play-player").click(function () {
        mode = "player";
        alert("Playing against another Player!");
    });
});

function updateBoard(board) {
    $(".cell").each(function (index) {
        $(this).text(board[index]);
    });
}
