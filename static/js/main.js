// Bob-QA Gatekeeper - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Auto-dismiss alerts after 5 seconds
    autoDismissAlerts();
    
    // Confirm dangerous actions
    confirmDangerousActions();
    
    // Add loading states to forms
    addFormLoadingStates();
    
    // Initialize code syntax highlighting
    highlightCodeBlocks();
    
    // Initialize dynamic mouse tracking blob
    initCursorBlob();
});

/**
 * Dynamic Mouse Tracking Blob
 */
function initCursorBlob() {
    const blob = document.getElementById('cursor-blob');
    if (!blob) return;
    
    window.addEventListener('pointermove', (e) => {
        const { clientX, clientY } = e;
        
        blob.animate({
            left: `${clientX}px`,
            top: `${clientY}px`
        }, { duration: 3000, fill: "forwards" });
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-dismiss alert messages after 5 seconds
 */
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Confirm dangerous actions (delete, reject, etc.)
 */
function confirmDangerousActions() {
    const dangerousForms = document.querySelectorAll('form[data-confirm]');
    dangerousForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const message = form.getAttribute('data-confirm') || 
                          'Are you sure you want to perform this action?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Add loading states to form submissions
 */
function addFormLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });
}

/**
 * Highlight code blocks
 */
function highlightCodeBlocks() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(block) {
        // Add line numbers
        const lines = block.textContent.split('\n');
        if (lines.length > 1) {
            block.classList.add('line-numbers');
        }
    });
}

/**
 * Copy code to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Code copied to clipboard!', 'success');
        }).catch(function(err) {
            console.error('Failed to copy:', err);
            showToast('Failed to copy code', 'error');
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showToast('Code copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy:', err);
            showToast('Failed to copy code', 'error');
        }
        document.body.removeChild(textarea);
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

/**
 * Create toast container if it doesn't exist
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

/**
 * Format date to relative time (e.g., "2 hours ago")
 */
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffSecs = Math.floor(diffMs / 1000);
    const diffMins = Math.floor(diffSecs / 60);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffSecs < 60) return 'just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    
    return date.toLocaleDateString();
}

/**
 * Update risk score display
 */
function updateRiskDisplay(value) {
    const display = document.getElementById('risk_display');
    if (display) {
        display.textContent = parseFloat(value).toFixed(2);
    }
}

/**
 * Filter table rows
 */
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = input.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
        }
    });
}

/**
 * Export table to CSV
 */
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csv = [];
    
    rows.forEach(function(row) {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        cols.forEach(function(col) {
            rowData.push('"' + col.textContent.replace(/"/g, '""') + '"');
        });
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * API Helper Functions
 */
const API = {
    baseUrl: '/api',
    
    async get(endpoint) {
        const response = await fetch(`${this.baseUrl}${endpoint}`);
        return await response.json();
    },
    
    async post(endpoint, data) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    },
    
    async put(endpoint, data) {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    }
};

// Export functions for use in templates
window.copyToClipboard = copyToClipboard;
window.updateRiskDisplay = updateRiskDisplay;
window.filterTable = filterTable;
window.exportTableToCSV = exportTableToCSV;
window.API = API;

// Made with Bob
