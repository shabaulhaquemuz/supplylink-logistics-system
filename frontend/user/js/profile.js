
// ## 📄 **js/profile.js**
// ```javascript
// // ================================================================
// // Profile Module - Displays user profile information
// // ================================================================

import { apiRequest, protectPage, logout } from './api.js';

// Protect this page
protectPage();

// Initialize profile page
document.addEventListener('DOMContentLoaded', async () => {
    setupEventListeners();
    await loadProfile();
});

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Logout button
    document.getElementById('logoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        logout();
    });
}

/**
 * Load user profile
 */
async function loadProfile() {
    try {
        document.getElementById('loadingSpinner').style.display = 'flex';
        document.getElementById('profileContent').style.display = 'none';
        
        const user = await apiRequest('/me', 'GET');
        
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('profileContent').style.display = 'block';
        
        displayProfile(user);
        
    } catch (error) {
        document.getElementById('loadingSpinner').style.display = 'none';
        console.error('Error loading profile:', error);
        alert('Failed to load profile. Please try again.');
    }
}

/**
 * Display profile information
 */
function displayProfile(user) {
    document.getElementById('profileName').textContent = user.full_name;
    document.getElementById('profileRole').textContent = capitalizeFirst(user.role);
    document.getElementById('profileEmail').textContent = user.email;
    document.getElementById('profilePhone').textContent = user.phone || 'Not provided';
    document.getElementById('profileCreated').textContent = formatDate(user.created_at);
    
    // Status
    const statusElement = document.getElementById('profileStatus');
    if (user.is_active) {
        statusElement.innerHTML = '<span class="status-active">● Active</span>';
    } else {
        statusElement.innerHTML = '<span style="color: var(--color-error);">● Inactive</span>';
    }
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        month: 'long', 
        day: 'numeric', 
        year: 'numeric'
    });
}

/**
 * Capitalize first letter
 */
function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}