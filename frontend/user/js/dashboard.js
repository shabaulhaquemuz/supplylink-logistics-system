// ## 📄 **js/dashboard.js**
// ```javascript
// // ================================================================
// // Dashboard Module - Loads and displays user shipments
// // ================================================================

import { apiRequest, protectPage, logout } from './api.js';

// Protect this page
protectPage();

let allShipments = [];
let currentFilter = 'all';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    setupEventListeners();
    await loadUserInfo();
    await loadShipments();
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
    
    // Filter tabs
    const filterTabs = document.querySelectorAll('.filter-tab');
    filterTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            filterTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentFilter = tab.getAttribute('data-filter');
            renderShipments();
        });
    });
}

/**
 * Load user information
 */
async function loadUserInfo() {
    try {
        const user = await apiRequest('/me', 'GET');
        document.getElementById('welcomeText').textContent = 
            `Welcome back, ${user.full_name}`;
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

/**
 * Load all shipments
 */
async function loadShipments() {
    try {
        document.getElementById('loadingSpinner').style.display = 'flex';
        document.getElementById('shipmentsContainer').style.display = 'none';
        document.getElementById('emptyState').style.display = 'none';
        
        allShipments = await apiRequest('/shipments', 'GET');
        
        document.getElementById('loadingSpinner').style.display = 'none';
        
        if (allShipments.length === 0) {
            document.getElementById('emptyState').style.display = 'flex';
        } else {
            document.getElementById('shipmentsContainer').style.display = 'grid';
            updateStats();
            renderShipments();
        }
        
    } catch (error) {
        document.getElementById('loadingSpinner').style.display = 'none';
        console.error('Error loading shipments:', error);
        alert('Failed to load shipments. Please try again.');
    }
}

/**
 * Update statistics
 */
function updateStats() {
    const stats = {
        pending: 0,
        inTransit: 0,
        delivered: 0,
        total: allShipments.length
    };
    
    allShipments.forEach(shipment => {
        const status = shipment.status.toUpperCase();
        if (status === 'PENDING') stats.pending++;
        else if (status === 'IN_TRANSIT' || status === 'PICKED_UP' || status === 'OUT_FOR_DELIVERY') stats.inTransit++;
        else if (status === 'DELIVERED') stats.delivered++;
    });
    
    document.getElementById('pendingCount').textContent = stats.pending;
    document.getElementById('inTransitCount').textContent = stats.inTransit;
    document.getElementById('deliveredCount').textContent = stats.delivered;
    document.getElementById('totalCount').textContent = stats.total;
}

/**
 * Render shipments based on filter
 */
function renderShipments() {
    const container = document.getElementById('shipmentsContainer');
    
    let filtered = allShipments;
    if (currentFilter !== 'all') {
        filtered = allShipments.filter(s => s.status.toUpperCase() === currentFilter);
    }
    
    if (filtered.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--color-text-muted); padding: 2rem;">No shipments found for this filter.</p>';
        return;
    }
    
    container.innerHTML = filtered.map(shipment => createShipmentCard(shipment)).join('');
}

/**
 * Create shipment card HTML
 */
function createShipmentCard(shipment) {
    const status = getStatusInfo(shipment.status);
    
    return `
        <div class="shipment-card" onclick="window.location.href='/tracking.html?id=${shipment.id}'">
            <div class="shipment-card-header">
                <div class="shipment-number">${shipment.shipment_number}</div>
                <div class="status-badge ${status.class}">
                    <span class="status-dot"></span>
                    <span class="status-text">${status.text}</span>
                </div>
            </div>
            
            <div class="shipment-route">
                <div class="route-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="10" r="3" stroke-width="2"/>
                        <path d="M12 21.7C17.3 17 20 13 20 10a8 8 0 1 0-16 0c0 3 2.7 7 8 11.7z" stroke-width="2"/>
                    </svg>
                </div>
                <div class="route-text">
                    <div class="route-label">From</div>
                    <div class="route-value">${shipment.pickup_location}</div>
                </div>
            </div>
            
            <div class="shipment-route">
                <div class="route-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke-width="2"/>
                        <polyline points="9 22 9 12 15 12 15 22" stroke-width="2"/>
                    </svg>
                </div>
                <div class="route-text">
                    <div class="route-label">To</div>
                    <div class="route-value">${shipment.delivery_location}</div>
                </div>
            </div>
            
            <div class="shipment-details">
                <div class="detail-item">
                    <div class="detail-label">Cargo Type</div>
                    <div class="detail-value">${shipment.cargo_type || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Weight</div>
                    <div class="detail-value">${shipment.weight ? shipment.weight + ' kg' : 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Total Price</div>
                    <div class="detail-value">$${shipment.total_price ? shipment.total_price.toFixed(2) : '0.00'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Created</div>
                    <div class="detail-value">${formatDate(shipment.created_at)}</div>
                </div>
            </div>
            
            <div class="shipment-card-footer">
                <a href="/tracking.html?id=${shipment.id}" class="btn-track" onclick="event.stopPropagation()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="10" stroke-width="2"/>
                        <polyline points="12 6 12 12 16 14" stroke-width="2"/>
                    </svg>
                    Track Shipment
                </a>
            </div>
        </div>
    `;
}

/**
 * Get status display information
 */
function getStatusInfo(status) {
    const statusUpper = status.toUpperCase();
    
    const statusMap = {
        'PENDING': { text: 'Pending', class: 'pending' },
        'PICKED_UP': { text: 'In Transit', class: 'in-transit' },
        'IN_TRANSIT': { text: 'In Transit', class: 'in-transit' },
        'OUT_FOR_DELIVERY': { text: 'Out for Delivery', class: 'in-transit' },
        'DELIVERED': { text: 'Delivered', class: 'delivered' },
        'FAILED': { text: 'Failed', class: 'pending' },
        'CANCELLED': { text: 'Cancelled', class: 'pending' }
    };
    
    return statusMap[statusUpper] || { text: status, class: 'pending' };
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}