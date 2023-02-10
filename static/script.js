window.onload = function() {
    const cells = Array.from(document.getElementsByClassName("cell"));
    const header = document.getElementById("header");
    var field;
    var gameId;

    function reloadField(obj) {
        field = obj.field;
        gameId = obj.gameId;
        cells.forEach((cell, index) => {
            cell.innerText = obj.field[index]
        });
        if (obj.hasOwnProperty('status'))
        {
            console.log(obj.status)
            header.innerText = 'Your move';
        } else {
            header.innerText = 'Waiting...';
        }
    }

    function action(index) {
        if (cells[index].innerText != 'X' && cells[index].innerText != 'O') {
            var player = 'O';
            if (field.split(" ").length % 2 == 0) {
                player = 'X'
            }
            field = field.substring(0,index) + player + field.substring(index+1);
            res = {};
            res.gameId = gameId;
            res.field = field;
            reloadField(res);
            

            var xhr = new XMLHttpRequest();
            xhr.open("POST", '/action', true);
            xhr.getResponseHeader("Content-type", "application/json");
            xhr.setRequestHeader("Content-type", "application/json");

            xhr.onload = function() {
                const obj = JSON.parse(this.responseText);
                reloadField(obj);
            }
            xhr.send(JSON.stringify(res));
        }
    }

    function start() {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/action', true);
        xhr.getResponseHeader("Content-type", "application/json");
        xhr.setRequestHeader("Content-type", "application/json");

        xhr.onload = function() {
            const obj = JSON.parse(this.responseText);
            reloadField(obj);
        }
        xhr.send('{"start":"OK"}');
    }

    cells.forEach((cell, index) => {
        cell.addEventListener('click', e => {
            action(index);
        });
    });

    start();
}