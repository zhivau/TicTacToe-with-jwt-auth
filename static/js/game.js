let game_web = {
    game_board: [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ],
    game_id: '',
    active_turn: 1,
    player1_id: '',
    player2_id: '',
    state: 'waiting',
    player1_sign: 'X',
    player2_sign: 'O',
    created_at: ''
};

let games_web = [];

function resetGame() {

    game_web = {
        game_board: [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ],
        game_id: '',
        active_turn: 1,
        player1_id: '',
        player2_id: '',
        state: 'waiting',
        player1_sign: 'X',
        player2_sign: 'O',
        created_at: ''
    };

    const startGameBtnCmp = document.getElementById('start-game-btn-cmp');
    const startGameBtnUsr = document.getElementById('start-game-btn-usr');
    const joinGameBtn = document.getElementById('join-game-btn');

    startGameBtnCmp.classList.remove('hidden');
    startGameBtnUsr.classList.remove('hidden');
    joinGameBtn.classList.remove('hidden');

    const gameForm = document.getElementById('game-form');
    renderGameBoard([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]);
    gameForm.classList.add('hidden');

    document.getElementById('game-over-message').classList.add('hidden');
}

function updateGame(position, symbol) {
    const [row, col] = position.split('-').map(Number);
    if (game_web.game_board[row][col] === ' ') {
        game_web.game_board[row][col] = symbol;
        return true;
    }
    return false;
}

async function sendGameState() {
    const response = await authorizedFetch(`/game/${game_web.game_id}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(game_web)
    });

    const data = await response.json();

    if (data.error) {
        alert('Error: ' + data.error);
    } else {
        game_web.game_board = data.game_board;
        game_web.state = data.state;
        game_web.active_turn = data.active_turn;
    }
}

async function startNewGameCmp() {
    const response = await authorizedFetch('/new_game/1');
    const data = await response.json();

    if (data.error) {
        throw new Error(data.error);
    } else {
        game_web.game_board = data.game_board;
        game_web.game_id = data.game_id;
        game_web.active_turn = data.active_turn;
        game_web.player1_id = data.player1_id;
        game_web.player2_id = data.player2_id;
        game_web.state = data.state;
    }
}

async function startNewGameUsr() {
    const response = await authorizedFetch('/new_game/2');
    const data = await response.json();

    if (data.error) {
        throw new Error(data.error);
    } else {
        game_web.game_board = data.game_board;
        game_web.game_id = data.game_id;
        game_web.active_turn = data.active_turn;
        game_web.player1_id = data.player1_id;
        game_web.player2_id = data.player2_id;
        game_web.state = data.state;

        gamePollingInterval = setInterval(pollGameState, 1000);
    }
}

async function pollGameState() {
    try {
        const response = await authorizedFetch(`/game_state/${game_web.game_id}`);
        const data = await response.json();

        game_web.game_board = data.game_board;
        game_web.game_id = data.game_id;

        game_web.active_turn = data.active_turn;
        game_web.player2_id = data.player2_id;
        game_web.state = data.state;

        renderGameBoard(game_web.game_board)

        if (isGameOver()) {
            document.getElementById('game-over-message').classList.remove('hidden');
            clearInterval(gamePollingInterval);
            setTimeout(() => resetGame(), 1000);
        }
    } catch (error) {
        console.error('Error fetching game state:', error);
    }
}


async function showAvailableGames() {
    const response = await authorizedFetch('/available_games');
    const data = await response.json();

    games_web = [];

    if (data.error) {
        throw new Error(data.error);
    } else {
        for (let gameId in data) {
            if (data.hasOwnProperty(gameId)) {
                let available_game = data[gameId];

                let available_game_web = {
                    game_board: available_game.game_board,
                    game_id: available_game.game_id,
                    active_turn: available_game.active_turn,
                    player1_id: available_game.player1_id,
                    player2_id: available_game.player2_id,
                    state: available_game.state,
                    player1_sign: available_game.player1_sign,
                    player2_sign: available_game.player2_sign
                };

                games_web.push(available_game_web);
            }
        }

        const buttonContainer = document.getElementById("game-buttons");
        games_web.forEach((av_game, index) => {
            const button = document.createElement("button");
            button.textContent = `${av_game.game_id}`;
            button.id = `game-btn-${index + 1}`;
            button.onclick = async function () {
                const response_join = await authorizedFetch(`/join_game/${av_game.game_id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(av_game)
                });

                const data_join = await response_join.json();

                if (data_join.error) {
                    alert('Error: ' + data_join.error);
                } else {
                    game_web.game_board = data_join.game_board;
                    game_web.game_id = data_join.game_id;
                    game_web.active_turn = data_join.active_turn;
                    game_web.player1_id = data_join.player1_id;
                    game_web.player2_id = data_join.player2_id;
                    game_web.state = data_join.state;
                    alert('Вы успешно присоединились к игре')

                    const gameForm = document.getElementById('game-form');
                    gameForm.classList.remove('hidden');

                    gamePollingInterval = setInterval(pollGameState, 1000);
                }
                buttonContainer.innerHTML = "";
                games_web = [];
            };

            buttonContainer.appendChild(button);
        });
    }
}

function renderGameBoard(gameBoard) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell) => {
        const [row, col] = cell.dataset.position.split('-').map(Number);
        cell.textContent = gameBoard[row][col];
    });
}

function isGameOver() {
    const gameOverStates = ['draw', 'win_player1', 'win_player2'];
    return gameOverStates.includes(game_web.state);
}

function chooseSymbol() {
    if (game_web.active_turn === 1) {
        return 'X';
    } else if (game_web.active_turn === 2) {
        return 'O';
    }
}

document.getElementById('game-form').addEventListener('click', async (event) => {
    if (!event.target.classList.contains('cell') || isGameOver()) return;

    const position = event.target.getAttribute('data-position');
    const symbol = chooseSymbol();

    if (updateGame(position, symbol)) {
        await sendGameState();
    }

    renderGameBoard(game_web.game_board)

    if (isGameOver()) {
        document.getElementById('game-over-message').classList.remove('hidden');
        clearInterval(gamePollingInterval);
        setTimeout(() => resetGame(), 1000);
    }
});

