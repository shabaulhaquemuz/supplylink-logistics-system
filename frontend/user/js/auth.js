// ## 📄 **js/auth.js**
// ```javascript
// // ================================================================
// // Authentication Module - Handles login and registration
// // ================================================================

import { apiRequest } from './api.js';
import { showError, showLoading, hideLoading } from './ui.js';

// Check which page we're on
const currentPage = window.location.pathname;

if (currentPage.includes('login.html')) {
    initLogin();
} else if (currentPage.includes('register.html')) {
    initRegister();
}

/**
 * Initialize Login Page
 */
function initLogin() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        
        try {
            showLoading(loginForm);
            
            // FastAPI expects form data for OAuth2
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
            
            const response = await fetch('http://localhost:8001/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }
            
            // Store token
            localStorage.setItem('token', data.access_token);
            
            // Redirect to dashboard
            window.location.href = '/dashboard.html';
            
        } catch (error) {
            hideLoading(loginForm);
            showError(error.message);
        }
    });
}

/**
 * Initialize Register Page
 */
function initRegister() {
    const registerForm = document.getElementById('registerForm');
    
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const full_name = document.getElementById('full_name').value.trim();
        const email = document.getElementById('email').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const password = document.getElementById('password').value;
        const confirm_password = document.getElementById('confirm_password').value;
        
        // Validate passwords match
        if (password !== confirm_password) {
            showError('Passwords do not match');
            return;
        }
        
        // Validate password length
        if (password.length < 8) {
            showError('Password must be at least 8 characters long');
            return;
        }
        
        try {
            showLoading(registerForm);
            
            const userData = {
                full_name,
                email,
                password,
            };
            
            if (phone) {
                userData.phone = phone;
            }
            
            await apiRequest('/register', 'POST', userData);
            
            // Auto-login after registration
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
            
            const loginResponse = await fetch('http://localhost:8001/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData
            });
            
            const loginData = await loginResponse.json();
            
            if (loginResponse.ok) {
                localStorage.setItem('token', loginData.access_token);
                window.location.href = '/dashboard.html';
            } else {
                // Registration successful but auto-login failed
                window.location.href = '/login.html';
            }
            
        } catch (error) {
            hideLoading(registerForm);
            showError(error.message);
        }
    });
}