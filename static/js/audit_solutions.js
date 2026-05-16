/**
 * Audit Solutions - JavaScript for handling AI-generated solutions
 */

// Copy solution code to clipboard
function copySolutionCode(solutionIndex, code) {
    navigator.clipboard.writeText(code).then(() => {
        showNotification('Code copied to clipboard.', 'success');
    }).catch(err => {
        showNotification('Failed to copy code.', 'error');
        console.error('Copy failed:', err);
    });
}

// Apply solution to audit
function applySolution(auditId, solutionData) {
    fetch(`/api/audits/${auditId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code_snippet: solutionData.code,
            ai_risk_score: solutionData.newRisk,
            human_approved: true,
            comments: `Applied AI Solution: ${solutionData.title}\n\nImprovement: ${solutionData.improvement}%\nOriginal Risk: ${solutionData.originalRisk} → New Risk: ${solutionData.newRisk}\n\nApproach: ${solutionData.approach}`
        })
    })
    .then(response => response.json())
    .then(data => {
        showNotification('Solution applied successfully.', 'success');
        setTimeout(() => location.reload(), 1500);
    })
    .catch(error => {
        showNotification('Error applying solution: ' + error.message, 'error');
        console.error('Apply error:', error);
    });
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips if available
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Made with Bob
