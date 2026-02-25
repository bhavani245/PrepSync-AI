// frontend/config.js
const API_BASE_URL = '/api'; // Uses relative path for both local and remote backends

// Add other configuration options here
const CONFIG = {
    API: {
        BASE_URL: API_BASE_URL,
        ENDPOINTS: {
            LOGIN: '/auth/login',
            REGISTER: '/auth/register',
            FORGOT_PASSWORD: '/auth/forgot-password',
            EXAMS: '/exams',
            UPCOMING_EXAMS: '/exams/upcoming'
        }
    },
    ROUTES: {
        HOME: 'index.html',
        LOGIN: 'login.html',
        REGISTER: 'registration.html',
        FORGOT_PASSWORD: 'forgot-password.html'
    }
};