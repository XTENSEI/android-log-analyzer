export class Tooltip {
    constructor(element) {
        this.element = element;
        this.tooltip = null;
    }

    show(text) {
        const rect = this.element.getBoundingClientRect();
        this.tooltip = document.createElement('div');
        this.tooltip.className = 'tooltip';
        this.tooltip.textContent = text;
        this.tooltip.style.cssText = `
            position: fixed;
            left: ${rect.left}px;
            top: ${rect.top - 30}px;
            background: #333;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
        `;
        document.body.appendChild(this.tooltip);
    }

    hide() {
        if (this.tooltip) {
            this.tooltip.remove();
            this.tooltip = null;
        }
    }
}

export default Tooltip;
