export class Modal {
    constructor() {
        this.element = null;
    }

    show(content, title = 'Dialog') {
        const html = `
            <div class="modal-overlay">
                <div class="modal">
                    <div class="modal-header">
                        <h3>${title}</h3>
                        <button class="close-btn">&times;</button>
                    </div>
                    <div class="modal-body">${content}</div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', html);
        this.element = document.querySelector('.modal-overlay');
        
        this.element.querySelector('.close-btn').addEventListener('click', () => this.hide());
        this.element.addEventListener('click', (e) => {
            if (e.target === this.element) this.hide();
        });
    }

    hide() {
        if (this.element) {
            this.element.remove();
            this.element = null;
        }
    }
}

export default Modal;
