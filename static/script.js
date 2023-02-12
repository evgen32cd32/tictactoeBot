window.onload = function() {
    const cells = Array.from(document.getElementsByClassName("cell"));
    const lvls = Array.from(document.getElementsByClassName("lvl"));
    const plts = Array.from(document.getElementsByClassName("player"));
    const lvl_button = document.getElementById("lvl_button");
    const player_button = document.getElementById("player_button");
    const new_game = document.getElementById("new_game");
    const header = document.getElementById("header");
    var field;
    var gameId;
    var gameover = false;

    function reloadField(obj) {
        field = obj.field;
        gameId = obj.gameId;
        cells.forEach((cell, index) => {
            cell.innerText = obj.field[index]
        });
        switch(obj.status)
        {
            case 'waiting':
                header.innerText = 'Waiting...';
                break;
            case 'player_move':
                header.innerText = 'Your turn';
                break;
            case 'cheater':
                header.innerText = 'Cheater!';
                break;
            case 'draw':
                header.innerText = 'Draw';
                gameover = true;
                break;
            case 'player_won':
                header.innerText = 'You won!';
                gameover = true;
                break;
            case 'bot_won':
                header.innerText = 'You lost!';
                gameover = true;
                break;
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
            res.status = 'waiting';
            res.player = player_button.innerText;
            res.lvl = lvl_button.innerText;
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
        res = {};
        res.start = "OK";
        res.player = player_button.innerText;
        res.lvl = lvl_button.innerText;
        xhr.send(JSON.stringify(res));
    }

    new_game.addEventListener('click', e => {
        gameover = false
        start();
    });

    lvls.forEach((lvl, index) => {
        lvl.addEventListener('click', e => {
            lvl_button.innerText = lvl.innerText;
        });
    });

    plts.forEach((plt, index) => {
        plt.addEventListener('click', e => {
            player_button.innerText = plt.innerText;
        });
    });

    cells.forEach((cell, index) => {
        cell.addEventListener('click', e => {
            if (!gameover)
            {
                action(index);
            }
        });
    });

    start();
}