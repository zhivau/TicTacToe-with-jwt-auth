async function handleLogin(event) {
    event.preventDefault();
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ login, password })
    });
    const data = await response.json();

    if (data.error) {
        alert('Error: ' + data.error);
    } else {
        alert('Welcome');
        tokens.accessToken = data.accessToken;
        tokens.refreshToken = data.refreshToken;
        showGame();
    }
}
