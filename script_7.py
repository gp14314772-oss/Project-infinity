# Create CSS and JavaScript files for styling and functionality

# CSS styles
css_content = '''/* Custom styles for Attendance System */

body {
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    border: none;
}

.card-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px 10px 0 0 !important;
}

.btn {
    border-radius: 5px;
}

.badge {
    font-size: 0.8em;
}

.table th {
    border-top: none;
    font-weight: 600;
    color: #495057;
}

.stats-card {
    transition: transform 0.2s;
}

.stats-card:hover {
    transform: translateY(-5px);
}

.verification-status {
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}

.verification-success {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: white;
}

.verification-warning {
    background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
    color: white;
}

.session-timeline {
    position: relative;
    padding-left: 30px;
}

.session-timeline::before {
    content: '';
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #dee2e6;
}

.timeline-item {
    position: relative;
    margin-bottom: 20px;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -25px;
    top: 5px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #007bff;
}

@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    .card {
        margin-bottom: 20px;
    }
}'''

# JavaScript functionality
js_content = '''// Attendance System JavaScript

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
}'''

# Save CSS and JS files
with open('static/css/style.css', 'w') as f:
    f.write(css_content)

with open('static/js/app.js', 'w') as f:
    f.write(js_content)

print("CSS and JavaScript files created:")
print("- static/css/style.css")
print("- static/js/app.js")