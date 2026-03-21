export class FilterPanel {
    constructor(container) {
        this.container = container;
    }

    render(filters, onChange) {
        let html = '<div class="filter-panel">';
        
        if (filters.severity) {
            html += this.renderSelect('severity', 'Severity', filters.severity);
        }
        
        if (filters.category) {
            html += this.renderSelect('category', 'Category', filters.category);
        }
        
        if (filters.tag) {
            html += this.renderInput('tag', 'Tag', filters.tag);
        }
        
        html += '<button class="apply-btn">Apply</button>';
        html += '</div>';
        
        this.container.innerHTML = html;
    }

    renderSelect(id, label, options) {
        return `
            <div class="filter-item">
                <label>${label}</label>
                <select id="${id}">
                    ${options.map(o => `<option value="${o}">${o}</option>`).join('')}
                </select>
            </div>
        `;
    }

    renderInput(id, label, value) {
        return `
            <div class="filter-item">
                <label>${label}</label>
                <input type="text" id="${id}" value="${value}">
            </div>
        `;
    }
}

export default FilterPanel;
