export class Loader {
    constructor(container) {
        this.container = container;
    }

    show(message = 'Loading...') {
        this.container.innerHTML = `
            <div class="loader">
                <div class="spinner"></div>
                <p>${message}</p>
            </div>
        `;
    }

    hide() {
        this.container.innerHTML = '';
    }
}

export default Loader;
