var gameCode = document.getElementById("game_board").getAttribute("game_code");
var char_choice = document.getElementById("game_board").getAttribute("char_choice");

var connectionString = 'ws://' + window.location.host + '/ws/' + gameCode + '/';
var gameSocket = new WebSocket(connectionString);


function update_player(index, player){

    let data = {
        'game_code': game_code,
        'user_id': player,
        'player_data': {
            "index": index,
            "player": player
        },
    }

    if(gameBoard[index] == -1){
        // if the valid move, update the gameboard
        // state and send the move to the server.
        moveCount++;
        if(player == 'X')
            gameBoard[index] = 1;
        else if(player == 'O')
            gameBoard[index] = 0;
        else{
            alert("Invalid character choice");
            return false;
        }
        gameSocket.send(JSON.stringify(data))
    }
    // place the move in the game box.
    elementArray[index].innerHTML = player;
}


// Main function which handles the connection
// of websocket.
function connect() {
    gameSocket.onopen = function open() {
        console.log('WebSockets connection created.');
        // on websocket open, send the START event.
        gameSocket.send(JSON.stringify({
            "event": "START",
            "message": ""
        }));
    };

    gameSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };
    // Sending the info about the room
    gameSocket.onmessage = function (e) {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data = JSON.parse(e.data);
        data = data["payload"];
        let message = data['message'];
        let event = data["event"];
        switch (event) {
            case "START":
                reset();
                break;
            case "END":
                alert(message);
                reset();
                break;
            case "MOVE":
                if(message["player"] != char_choice){
                    make_move(message["index"], message["player"])
                    myturn = true;
                    document.getElementById("alert_move").style.display = 'inline';
                }
                break;
            default:
                console.log("No event")
        }
    };

    if (gameSocket.readyState == WebSocket.OPEN) {
        gameSocket.onopen();
    }
}

//call the connect function at the start.
connect();