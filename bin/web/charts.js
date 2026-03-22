export class ChartRenderer {
    constructor(container) {
        this.container = container;
    }

    renderBarChart(data, options = {}) {
        const { width = 400, height = 200, color = '#3b82f6' } = options;
        
        const max = Math.max(...data.map(d => d.value));
        
        let html = `<div style="width: ${width}px;">`;
        for (const item of data) {
            const barWidth = (item.value / max) * 100;
            html += `
                <div style="margin: 4px 0;">
                    <span style="display: inline-block; width: 80px;">${item.label}</span>
                    <div style="display: inline-block; width: ${barWidth}%; height: 20px; background: ${color};"></div>
                    <span>${item.value}</span>
                </div>
            `;
        }
        html += '</div>';
        
        this.container.innerHTML = html;
    }

    renderPieChart(data, options = {}) {
        const { size = 200 } = options;
        
        let html = `<div style="width: ${size}px; height: ${size}px; border-radius: 50%; background: conic-gradient(${this.generateGradient(data)});"></div>`;
        html += '<div style="margin-top: 10px;">';
        
        const colors = ['#ef4444', '#f59e0b', '#22c55e', '#3b82f6', '#8b5cf6'];
        data.forEach((item, i) => {
            html += `<div><span style="display: inline-block; width: 12px; height: 12px; background: ${colors[i % colors.length]};"></span> ${item.label}: ${item.value}</div>`;
        });
        html += '</div>';
        
        this.container.innerHTML = html;
    }

    generateGradient(data) {
        const colors = ['#ef4444', '#f59e0b', '#22c55e', '#3b82f6', '#8b5cf6'];
        let current = 0;
        return data.map((item, i) => {
            const next = current + (item.value / data.reduce((a, b) => a + b.value, 0)) * 100;
            const result = `${colors[i % colors.length]} ${current}% ${next}%`;
            current = next;
            return result;
        }).join(', ');
    }
}

export default ChartRenderer;
