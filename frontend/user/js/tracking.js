// ## 📄 **js/tracking.js**
// ```javascript
// // ================================================================
// // Tracking Module - Displays shipment tracking information
// // ================================================================

import { apiRequest, protectPage, logout } from './api.js';

// Protect this page
protectPage();

let shipmentId = null;

// Initialize tracking page
document.addEventListener('DOMContentLoaded', async () => {
    // Get shipment ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    shipmentId = urlParams.get('id');
    
    if (!shipmentId) {
        alert('No shipment ID provided');
        window.location.href = '/dashboard.html';
        return;
    }
    
    setupEventListeners();
    await loadTrackingData();
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
 * Load shipment and tracking data
 */
async function loadTrackingData() {
    try {
        document.getElementById('loadingSpinner').style.display = 'flex';
        document.getElementById('trackingContent').style.display = 'none';
        
        // Load shipment details
        const shipment = await apiRequest(`/shipments/${shipmentId}`, 'GET');
        
        // Load tracking history
        let trackingData = [];
        try {
            trackingData = await apiRequest(`/shipments/${shipmentId}/tracking`, 'GET');
        } catch (error) {
            console.log('No tracking data available yet');
        }
        
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('trackingContent').style.display = 'block';
        
        displayShipmentInfo(shipment);
        displayTrackingTimeline(trackingData);
        
    } catch (error) {
        document.getElementById('loadingSpinner').style.display = 'none';
        console.error('Error loading tracking data:', error);
        alert('Failed to load tracking information. Please try again.');
        window.location.href = '/dashboard.html';
    }
}

/**
 * Display shipment information
 */
function displayShipmentInfo(shipment) {
    // Shipment number and status
    document.getElementById('shipmentNumber').textContent = shipment.shipment_number;
    
    const status = getStatusInfo(shipment.status);
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.className = `status-badge ${status.class}`;
    statusBadge.innerHTML = `
        <span class="status-dot"></span>
        <span class="status-text">${status.text}</span>
    `;
    
    // Locations
    document.getElementById('pickupLocation').textContent = shipment.pickup_location;
    document.getElementById('deliveryLocation').textContent = shipment.delivery_location;
    
    // Info cards
    document.getElementById('cargoType').textContent = shipment.cargo_type || 'Not specified';
    document.getElementById('weight').textContent = shipment.weight ? `${shipment.weight} kg` : 'Not specified';
    document.getElementById('dimensions').textContent = shipment.dimensions || 'Not specified';
    document.getElementById('totalPrice').textContent = shipment.total_price ? `$${shipment.total_price.toFixed(2)}` : 'Not available';
    
    // COD status
    if (shipment.is_cod) {
        document.getElementById('codStatus').textContent = 
            `COD $${shipment.cod_amount.toFixed(2)} - ${shipment.cod_status || 'Pending'}`;
    } else {
        document.getElementById('codStatus').textContent = 'Not COD';
    }
    
    // Estimated delivery
    if (shipment.estimated_delivery) {
        document.getElementById('estimatedDelivery').textContent = 
            formatDateTime(shipment.estimated_delivery);
    } else {
        document.getElementById('estimatedDelivery').textContent = 'Not available';
    }
}

/**
 * Display tracking timeline
 */
function displayTrackingTimeline(trackingData) {
    const timeline = document.getElementById('trackingTimeline');
    const noTracking = document.getElementById('noTracking');
    
    if (!trackingData || trackingData.length === 0) {
        timeline.style.display = 'none';
        noTracking.style.display = 'block';
        return;
    }
    
    timeline.style.display = 'block';
    noTracking.style.display = 'none';
    
    timeline.innerHTML = trackingData.map((item, index) => `
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
                <div class="timeline-header">
                    <div class="timeline-status">${item.status_update || 'Status Update'}</div>
                    <div class="timeline-time">${formatDateTime(item.timestamp)}</div>
                </div>
                ${item.location_name ? `
                    <div class="timeline-location">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <circle cx="12" cy="10" r="3" stroke-width="2"/>
                            <path d="M12 21.7C17.3 17 20 13 20 10a8 8 0 1 0-16 0c0 3 2.7 7 8 11.7z" stroke-width="2"/>
                        </svg>
                        <span>${item.location_name}</span>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

/**
 * Get status display information
 */
function getStatusInfo(status) {
    const statusUpper = status.toUpperCase();
    
    const statusMap = {
        'PENDING': { text: 'Pending', class: 'pending' },
        'PICKED_UP': { text: 'Picked Up', class: 'in-transit' },
        'IN_TRANSIT': { text: 'In Transit', class: 'in-transit' },
        'OUT_FOR_DELIVERY': { text: 'Out for Delivery', class: 'in-transit' },
        'DELIVERED': { text: 'Delivered', class: 'delivered' },
        'FAILED': { text: 'DeliveryFailed', class: 'pending' },
'CANCELLED': { text: 'Cancelled', class: 'pending' }
};return statusMap[statusUpper] || { text: status, class: 'pending' };}