export class Router {
    constructor() {
        this.routes = {};
        window.addEventListener('popstate', () => this.handleRoute());
    }

    add(path, handler) {
        this.routes[path] = handler;
    }

    navigate(path) {
        window.history.pushState({}, '', path);
        this.handleRoute();
    }

    handleRoute() {
        const path = window.location.pathname;
        const handler = this.routes[path] || this.routes['/'];
        if (handler) handler();
    }
}

export default Router;
