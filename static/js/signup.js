async function handleSignup(event) {
    event.preventDefault();
    const login = document.getElementById('signup-login').value;
    const password = document.getElementById('signup-password').value;

    const response = await fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password })
    });
    const data = await response.json();

    if (data.error) {
        alert('Error: ' + data.error);
    } else {
        alert('Registration successful');
        showLogin();
    }
}
