async function loadUserProfile() {
    if (tokens.accessToken && tokens.refreshToken) {
        const response = await fetch(`/user`, {
            headers: {'Authorization': 'Bearer ' + tokens.accessToken}
        });
        const data = await response.json();

        if (response.ok) {
            document.getElementById('user-id').textContent = data.user_id;
            document.getElementById('user-login').textContent = data.login;
        } else {
            alert(data.error);
        }
    }
}
