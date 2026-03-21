export class Dropdown {
    constructor(container) {
        this.container = container;
    }

    render(options, selected, onChange) {
        let html = '<select class="dropdown">';
        
        for (const opt of options) {
            const sel = opt.value === selected ? 'selected' : '';
            html += `<option value="${opt.value}" ${sel}>${opt.label}</option>`;
        }
        
        html += '</select>';
        this.container.innerHTML = html;
        
        this.container.querySelector('select').addEventListener('change', (e) => {
            onChange(e.target.value);
        });
    }
}

export default Dropdown;
