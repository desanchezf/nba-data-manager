// Dashboard JavaScript functionality with theme support
class DashboardManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupNotifications();
        this.loadTheme();
    }

    setupEventListeners() {
        // Auto-dismiss alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    setupNotifications() {
        // Create notification container if it doesn't exist
        if (!document.getElementById('notification-container')) {
            const container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('dashboard-theme') || 'light';
        this.setTheme(savedTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('dashboard-theme', theme);

        const themeIcon = document.querySelector('.theme-icon');
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    showNotification(message, type = 'info') {
        const container = document.getElementById('notification-container');
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.innerHTML = `
            <i class="fas fa-${this.getIconForType(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        container.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    getIconForType(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    async executeAction(url, button) {
        const actionText = button.querySelector('.action-text');
        const loading = button.querySelector('.loading');
        const originalText = actionText.textContent;

        try {
            // Show loading state
            actionText.textContent = 'Ejecutando...';
            loading.classList.add('show');
            button.disabled = true;

            // Execute action
            const response = await fetch(`/${url}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.showNotification(data.message, 'success');
            } else {
                this.showNotification(data.message, 'danger');
            }

        } catch (error) {
            console.error('Error:', error);
            let errorMessage = 'Error inesperado';

            if (error.message.includes('Unexpected token')) {
                errorMessage = 'Error del servidor: respuesta no válida';
            } else if (error.message.includes('Failed to fetch')) {
                errorMessage = 'Error de conexión con el servidor';
            } else {
                errorMessage = error.message;
            }

            this.showNotification(errorMessage, 'danger');
        } finally {
            // Restore button state
            actionText.textContent = originalText;
            loading.classList.remove('show');
            button.disabled = false;
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dashboardManager = new DashboardManager();

    // Setup action buttons
    const actionButtons = document.querySelectorAll('[data-action]');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            window.dashboardManager.executeAction(url, this);
        });
    });
});

// Global functions
function executeAction(url, button) {
    if (window.dashboardManager) {
        window.dashboardManager.executeAction(url, button);
    }
}

function toggleTheme() {
    if (window.dashboardManager) {
        window.dashboardManager.toggleTheme();
    }
}
