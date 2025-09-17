// Attendance System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-refresh for active sessions
    const currentPath = window.location.pathname;
    if (currentPath.includes('/session/')) {
        setInterval(function() {
            // Check if session is still active and refresh if needed
            const statusBadge = document.querySelector('.badge');
            if (statusBadge && statusBadge.textContent.includes('Active')) {
                // Auto-refresh every 30 seconds for active sessions
                setTimeout(() => {
                    window.location.reload();
                }, 30000);
            }
        }, 1000);
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states to buttons
    document.querySelectorAll('button[type="submit"], .btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit') {
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                this.disabled = true;
            }
        });
    });

    // Real-time clock
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const dateString = now.toLocaleDateString();

        const clockElement = document.getElementById('live-clock');
        if (clockElement) {
            clockElement.innerHTML = `
                <i class="fas fa-clock"></i> 
                ${timeString} - ${dateString}
            `;
        }
    }

    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock(); // Initial call

    // Confirmation dialogs for important actions
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to perform this action?')) {
                e.preventDefault();
            }
        });
    });

    // Session status updates
    function updateSessionStatus() {
        const sessionCards = document.querySelectorAll('[data-session-id]');
        sessionCards.forEach(card => {
            const sessionId = card.dataset.sessionId;
            // Here you would make an AJAX call to check session status
            // For now, we'll just add visual indicators
        });
    }

    // Update session status every 10 seconds
    setInterval(updateSessionStatus, 10000);
});

// Utility functions
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// API helper functions
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showAlert('An error occurred. Please try again.', 'danger');
        throw error;
    }
}