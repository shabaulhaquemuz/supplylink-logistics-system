// ## 📄 **js/shipments.js**
// ```javascript
// // ================================================================
// // Shipments Module - Handles shipment creation
// // ================================================================

import { apiRequest, protectPage, logout } from './api.js';
import { showError, showLoading, hideLoading } from './ui.js';

// Protect this page
protectPage();

// Initialize form
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
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
    
    // COD checkbox
    const codCheckbox = document.getElementById('is_cod');
    const codAmountGroup = document.getElementById('codAmountGroup');
    
    codCheckbox.addEventListener('change', (e) => {
        if (e.target.checked) {
            codAmountGroup.style.display = 'block';
            document.getElementById('cod_amount').required = true;
        } else {
            codAmountGroup.style.display = 'none';
            document.getElementById('cod_amount').required = false;
            document.getElementById('cod_amount').value = '';
        }
    });
    
    // Weight input - show price estimate
    const weightInput = document.getElementById('weight');
    weightInput.addEventListener('input', updatePriceEstimate);
    
    // Form submission
    const shipmentForm = document.getElementById('shipmentForm');
    shipmentForm.addEventListener('submit', handleSubmit);
}

/**
 * Update price estimate based on weight
 */
function updatePriceEstimate() {
    const weight = parseFloat(document.getElementById('weight').value) || 0;
    
    if (weight > 0) {
        // Calculate using same logic as backend
        const basePrice = 50 + (weight * 2);
        const fuelSurcharge = basePrice * 0.15;
        const totalPrice = basePrice + fuelSurcharge;
        
        document.getElementById('basePrice').textContent = `$${basePrice.toFixed(2)}`;
        document.getElementById('fuelSurcharge').textContent = `$${fuelSurcharge.toFixed(2)}`;
        document.getElementById('totalPrice').textContent = `$${totalPrice.toFixed(2)}`;
        document.getElementById('priceEstimate').style.display = 'block';
    } else {
        document.getElementById('priceEstimate').style.display = 'none';
    }
}

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    
    // Gather form data
    const shipmentData = {
        pickup_location: document.getElementById('pickup_location').value.trim(),
        delivery_location: document.getElementById('delivery_location').value.trim(),
        cargo_type: document.getElementById('cargo_type').value || null,
        weight: parseFloat(document.getElementById('weight').value) || null,
        dimensions: document.getElementById('dimensions').value.trim() || null,
        is_home_pickup: document.getElementById('is_home_pickup').checked,
        is_home_delivery: document.getElementById('is_home_delivery').checked,
        is_cod: document.getElementById('is_cod').checked,
        cod_amount: null,
        estimated_delivery: null
    };
    
    // Add COD amount if applicable
    if (shipmentData.is_cod) {
        const codAmount = parseFloat(document.getElementById('cod_amount').value);
        if (!codAmount || codAmount <= 0) {
            showError('Please enter a valid COD amount');
            return;
        }
        shipmentData.cod_amount = codAmount;
    }
    
    // Add estimated delivery if provided
    const estimatedDelivery = document.getElementById('estimated_delivery').value;
    if (estimatedDelivery) {
        shipmentData.estimated_delivery = new Date(estimatedDelivery).toISOString();
    }
    
    try {
        showLoading(form);
        
        const result = await apiRequest('/shipments', 'POST', shipmentData);
        
        // Success! Redirect to tracking page
        window.location.href = `/tracking.html?id=${result.id}`;
        
    } catch (error) {
        hideLoading(form);
        showError(error.message || 'Failed to create shipment. Please try again.');
    }
}