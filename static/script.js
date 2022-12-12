window.onload = function() {
    const cells = document.getElementsByClassName("cell");
    var gameId;

    function reloadField(obj) {
        gameId = obj.gameId;

        score.innerText = obj.totalScore;
        turn.innerText = obj.turnNumber;

        Array.from(cells).forEach((cell, index) => {
            const x = Math.floor(index / 4);
            const y = index % 4;

            const val = obj.gameField[x][y];
            cell.innerText = val == 0 ? '' : val;
            cell.style.background = getColoring(val);
            resizeToFit(cell);
        });

        if (obj.gameOver == true) {
            document.getElementById("over").style.display = 'inline';
            document.onkeydown = function(e) { }
            field.addEventListener('touchstart', e => {});
            field.addEventListener('touchend', e => {});
        }
    }

    function start() {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/action', true);
        xhr.getResponseHeader("Content-type", "application/json");
        xhr.setRequestHeader("Content-type", "application/json");

        xhr.onload = function() {
            const obj = JSON.parse(this.responseText);
            console.log(obj);
            //reloadField(obj);
        }
        xhr.send('{"document":"hi"}');
    }

    start();
}