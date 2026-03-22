export class Tabs {
    constructor(container) {
        this.container = container;
        this.activeTab = 0;
    }

    render(tabs) {
        let html = '<div class="tabs">';
        
        html += '<div class="tab-headers">';
        tabs.forEach((tab, i) => {
            html += `<button class="tab-header ${i === this.activeTab ? 'active' : ''}">${tab.title}</button>`;
        });
        html += '</div>';
        
        html += '<div class="tab-contents">';
        tabs.forEach((tab, i) => {
            html += `<div class="tab-content" style="display: ${i === this.activeTab ? 'block' : 'none'}">${tab.content}</div>`;
        });
        html += '</div>';
        
        html += '</div>';
        this.container.innerHTML = html;
        
        this.container.querySelectorAll('.tab-header').forEach((btn, i) => {
            btn.addEventListener('click', () => this.switchTab(i));
        });
    }

    switchTab(index) {
        this.activeTab = index;
        this.container.querySelectorAll('.tab-header').forEach((btn, i) => {
            btn.classList.toggle('active', i === index);
        });
        this.container.querySelectorAll('.tab-content').forEach((content, i) => {
            content.style.display = i === index ? 'block' : 'none';
        });
    }
}

export default Tabs;
