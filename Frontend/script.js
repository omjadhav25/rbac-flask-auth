const apiUrl = 'http://localhost:5002'; // Backend API URL

// Register user
document.getElementById('register-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const role = document.getElementById('role').value;

    const response = await fetch(`${apiUrl}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, role })
    });

    const data = await response.json();
    alert(data.msg);
    window.location.href = 'login.html';
});

// Login user
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${apiUrl}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        window.location.href = 'dashboard.html';
    } else {
        alert('Login failed. Please check your credentials.');
    }
});

// Dashboard page
window.onload = async function() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }

    const response = await fetch(`${apiUrl}/dashboard`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    });

    const data = await response.json();
    if (data.msg) {
        document.getElementById('dashboard-msg').innerText = data.msg;
    }
};

// Logout user
function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}
