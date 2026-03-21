export class TableRenderer {
    constructor(container) {
        this.container = container;
    }

    render(columns, data) {
        let html = '<table class="data-table"><thead><tr>';
        
        for (const col of columns) {
            html += `<th>${col.title}</th>`;
        }
        
        html += '</tr></thead><tbody>';
        
        for (const row of data) {
            html += '<tr>';
            for (const col of columns) {
                const value = row[col.key];
                html += `<td>${this.formatValue(value, col.type)}</td>`;
            }
            html += '</tr>';
        }
        
        html += '</tbody></table>';
        this.container.innerHTML = html;
    }

    formatValue(value, type) {
        switch (type) {
            case 'number': return value.toLocaleString();
            case 'severity': return `<span class="severity-${value.toLowerCase()}">${value}</span>`;
            default: return value;
        }
    }
}

export default TableRenderer;
