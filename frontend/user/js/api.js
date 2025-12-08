// // ## 📄 **js/api.js**
// ```javascript
// // ================================================================
// // API Module - Handles all API requests with JWT authentication
// // ================================================================

const API_BASE = 'http://localhost:8001';

/**
 * Generic API request wrapper with JWT authentication
 */
export async function apiRequest(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        method,
        headers,
    };
    
    if (body && method !== 'GET') {
        config.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, config);
        
        // Handle 401 Unauthorized - redirect to login
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login.html';
            throw new Error('Unauthorized - please login again');
        }
        
        // Handle 204 No Content
        if (response.status === 204) {
            return null;
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

/**
 * Logout user
 */
export function logout() {
    localStorage.removeItem('token');
    window.location.href = '/index.html';
}

/**
 * Protect page - redirect to login if not authenticated
 */
export function protectPage() {
    if (!isAuthenticated()) {
        window.location.href = '/login.html';
    }
}