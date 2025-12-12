import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true, // Important for HTTP-only cookies
    headers: {
        'Content-Type': 'application/json',
    },
});

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            // Server responded with error
            const message = error.response.data?.detail || 'An error occurred';
            console.error('API Error:', message);

            // Handle 401 Unauthorized
            if (error.response.status === 401) {
                // Could redirect to login or dispatch logout action
                window.dispatchEvent(new CustomEvent('auth:unauthorized'));
            }
        } else if (error.request) {
            // Request made but no response
            console.error('Network Error: No response from server');
        } else {
            console.error('Error:', error.message);
        }

        return Promise.reject(error);
    }
);

export default api;
