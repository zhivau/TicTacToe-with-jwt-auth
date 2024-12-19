async function showCompletedGames() {
    if (tokens.accessToken && tokens.refreshToken) {
        const response = await authorizedFetch('/completed_games');
        const data = await response.json();

        let completed_games_web = [];
        document.getElementById('game-history').innerHTML = '';

        if (data.error) {
            throw new Error(data.error);
        } else {
            for (let gameId in data) {
                if (data.hasOwnProperty(gameId)) {
                    let completed_game = data[gameId];

                    let completed_game_web = {
                        game_board: completed_game.game_board,
                        game_id: completed_game.game_id,
                        active_turn: completed_game.active_turn,
                        player1_id: completed_game.player1_id,
                        player2_id: completed_game.player2_id,
                        state: completed_game.state,
                        player1_sign: completed_game.player1_sign,
                        player2_sign: completed_game.player2_sign,
                        created_at: completed_game.created_at,
                    };

                    completed_games_web.push(completed_game_web);
                }
            }
            const gameHistoryElement = document.getElementById('game-history');

            completed_games_web.forEach((cp_game) => {
                const listItem = document.createElement('li');
                listItem.textContent = "created_at: " + cp_game.created_at + " | " + "game id: " + cp_game.game_id + " | "
                    + "p1_id: " + cp_game.player1_id + " | " + "p2_id: " + cp_game.player2_id + " | "
                    + "state: " + cp_game.state;
                gameHistoryElement.prepend(listItem);
            });
        }
    }
}
