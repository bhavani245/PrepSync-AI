// frontend/js/auth.js

// Check if user is authenticated
export function isAuthenticated() {
    return !!localStorage.getItem('authToken');
}

// Get current user
export function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

// Logout function
export function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    window.location.href = './login.html';
}

// Get auth headers for API calls
export function getAuthHeaders() {
    const token = localStorage.getItem('authToken');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
}

// Redirect if not authenticated
export function requireAuth() {
    if (!isAuthenticated() && !window.location.pathname.endsWith('login.html') && 
        !window.location.pathname.endsWith('registration.html') &&
        !window.location.pathname.endsWith('forgot-password.html')) {
        window.location.href = './login.html';
    }
}

// Update navigation based on auth status
export function updateNavigation() {
    const isLoggedIn = isAuthenticated();
    const authLinks = document.getElementById('auth-links');
    const userMenu = document.getElementById('user-menu');
    
    if (authLinks) {
        if (isLoggedIn) {
            const user = getCurrentUser();
            authLinks.innerHTML = `
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        ${user?.username || 'User'}
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="./profile.html">Profile</a></li>
                        <li><a class="dropdown-item" href="./settings.html">Settings</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#" id="logout-btn">Logout</a></li>
                    </ul>
                </li>
            `;
            
            // Add logout event listener
            document.getElementById('logout-btn')?.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        } else {
            authLinks.innerHTML = `
                <li class="nav-item">
                    <a class="nav-link" href="./login.html">Login</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="./registration.html">Register</a>
                </li>
            `;
        }
    }
}

// Initialize auth
document.addEventListener('DOMContentLoaded', () => {
    updateNavigation();
    requireAuth();
});