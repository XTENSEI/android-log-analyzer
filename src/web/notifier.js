export class Notifier {
    constructor() {
        this.container = null;
    }

    init(containerId) {
        this.container = document.getElementById(containerId);
    }

    success(message) {
        this.show(message, 'success');
    }

    error(message) {
        this.show(message, 'error');
    }

    warning(message) {
        this.show(message, 'warning');
    }

    info(message) {
        this.show(message, 'info');
    }

    show(message, type) {
        const colors = {
            success: '#22c55e',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        
        const notification = document.createElement('div');
        notification.style.cssText = `
            padding: 12px 20px;
            margin: 8px 0;
            border-radius: 6px;
            background: ${colors[type]};
            color: white;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        this.container.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

export default Notifier;
