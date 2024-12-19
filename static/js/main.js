let tokens = {
    accessToken: '',
    refreshToken: ''
};

let gamePollingInterval;

async function authorizedFetch(url, options = {}) {
    options.headers = options.headers || {};

    if (tokens.accessToken && tokens.refreshToken) {
        options.headers['Authorization'] = 'Bearer ' + tokens.accessToken;
    }

    return fetch(url, options);
}

function showLogin() {
    document.getElementById('login-section').classList.remove('hidden');
    document.getElementById('history-section').classList.add('hidden');
    document.getElementById('leader-board-section').classList.add('hidden');
    document.getElementById('signup-section').classList.add('hidden');
    document.getElementById('game-section').classList.add('hidden');
    document.getElementById('profile-section').classList.add('hidden');

    clearInterval(gamePollingInterval);
}

function showSignup() {
    document.getElementById('signup-section').classList.remove('hidden');
    document.getElementById('history-section').classList.add('hidden');
    document.getElementById('leader-board-section').classList.add('hidden');
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('game-section').classList.add('hidden');
    document.getElementById('profile-section').classList.add('hidden');

    clearInterval(gamePollingInterval);
}

function showGame() {
    document.getElementById('game-section').classList.remove('hidden');
    document.getElementById('history-section').classList.add('hidden');
    document.getElementById('leader-board-section').classList.add('hidden');
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('signup-section').classList.add('hidden');
    document.getElementById('profile-section').classList.add('hidden');

    clearInterval(gamePollingInterval);

    const startGameBtnCmp = document.getElementById('start-game-btn-cmp');
    const startGameBtnUsr = document.getElementById('start-game-btn-usr');
    const joinGameBtn = document.getElementById('join-game-btn');
    const gameForm = document.getElementById('game-form');

    startGameBtnCmp.classList.remove('hidden');
    startGameBtnUsr.classList.remove('hidden');
    joinGameBtn.classList.remove('hidden');
    document.getElementById("game-buttons").innerHTML = "";
    gameForm.classList.add('hidden');
}

async function showProfile() {

    document.getElementById('profile-section').classList.remove('hidden');
    document.getElementById('history-section').classList.add('hidden');
    document.getElementById('leader-board-section').classList.add('hidden');
    document.getElementById('signup-section').classList.add('hidden');
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('game-section').classList.add('hidden');

    clearInterval(gamePollingInterval);
    await loadUserProfile();
}

async function showHistory() {
    document.getElementById('profile-section').classList.add('hidden');
    document.getElementById('history-section').classList.remove('hidden');
    document.getElementById('leader-board-section').classList.add('hidden');
    document.getElementById('signup-section').classList.add('hidden');
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('game-section').classList.add('hidden');

    clearInterval(gamePollingInterval);
    await showCompletedGames();
}

async function showLeaderBoard() {
    document.getElementById('profile-section').classList.add('hidden');
    document.getElementById('history-section').classList.add('hidden');
    document.getElementById('leader-board-section').classList.remove('hidden');
    document.getElementById('signup-section').classList.add('hidden');
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('game-section').classList.add('hidden');

    clearInterval(gamePollingInterval);
    await showLeaderUsers();
}

async function test() {
    const response = await fetch('/test');
    const data = await response.json();
    console.log(data.test + 5);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('signup-form').addEventListener('submit', handleSignup);

    const startGameBtnCmp = document.getElementById('start-game-btn-cmp');
    const startGameBtnUsr = document.getElementById('start-game-btn-usr');
    const joinGameBtn = document.getElementById('join-game-btn');
    const gameForm = document.getElementById('game-form');

    startGameBtnCmp.addEventListener(
        'click',
        async () => {
            startGameBtnCmp.disabled = true;
            startGameBtnUsr.disabled = true;
            joinGameBtn.disabled = true;
            try {
                await startNewGameCmp();
                startGameBtnCmp.classList.add('hidden');
                startGameBtnUsr.classList.add('hidden');
                joinGameBtn.classList.add('hidden');
                gameForm.classList.remove('hidden');
            } catch (error) {
                alert('Ошибка при создании новой игры:' + error);
            } finally {
                startGameBtnCmp.disabled = false;
                startGameBtnUsr.disabled = false;
                joinGameBtn.disabled = false;
            }
        }
    );

    startGameBtnUsr.addEventListener(
        'click',
        async () => {
            startGameBtnCmp.disabled = true;
            startGameBtnUsr.disabled = true;
            joinGameBtn.disabled = true;
            try {
                await startNewGameUsr();
                startGameBtnCmp.classList.add('hidden');
                startGameBtnUsr.classList.add('hidden');
                joinGameBtn.classList.add('hidden');
                gameForm.classList.remove('hidden');
            } catch (error) {
                alert('Ошибка при создании новой игры:' + error);
            } finally {
                startGameBtnCmp.disabled = false;
                startGameBtnUsr.disabled = false;
                joinGameBtn.disabled = false;
            }
        }
    );

    joinGameBtn.addEventListener(
        'click',
        async () => {
            startGameBtnCmp.disabled = true;
            startGameBtnUsr.disabled = true;
            joinGameBtn.disabled = true;
            try {
                await showAvailableGames();
                startGameBtnCmp.classList.add('hidden');
                startGameBtnUsr.classList.add('hidden');
                joinGameBtn.classList.add('hidden');
            } catch (error) {
                alert('Ошибка при создании новой игры:' + error);
            } finally {
                startGameBtnCmp.disabled = false;
                startGameBtnUsr.disabled = false;
                joinGameBtn.disabled = false;
            }
        }
    );
});
