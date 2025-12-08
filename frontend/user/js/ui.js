// ## 📄 **js/ui.js**
// ```javascript
// // ================================================================
// // UI Helper Functions
// // ================================================================

/**
 * Show error message
 */
export function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    } else {
        alert(message);
    }
}

/**
 * Show loading state on form
 */
export function showLoading(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        if (btnText) btnText.style.display = 'none';
        if (btnLoader) btnLoader.style.display = 'inline-flex';
    }
}

/**
 * Hide loading state on form
 */
export function hideLoading(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = false;
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        if (btnText) btnText.style.display = 'inline';
        if (btnLoader) btnLoader.style.display = 'none';
    }
}