async function showLeaderUsers() {
    if (tokens.accessToken && tokens.refreshToken) {
        const response = await authorizedFetch('/leaderboard/5');
        const data = await response.json();

        let leaderboard_users = [];
        document.getElementById('leader-board').innerHTML = '';

        if (data.error) {
            throw new Error(data.error);
        } else {
            for (let ind in data) {
                if (data.hasOwnProperty(ind)) {
                    let user_board = data[ind];
                    leaderboard_users.push(user_board);
                }
            }
            const leaderboardElement = document.getElementById('leader-board');

            leaderboard_users.forEach((us_board, index) => {
                const listItem = document.createElement('li');
                listItem.textContent = (index + 1) + ")  uuid: " + us_board.uuid +
                    " | " + "win/lose_draw: " + us_board.win + "/" + us_board.lose_draw
                leaderboardElement.append(listItem);
            });
        }
    }
}
