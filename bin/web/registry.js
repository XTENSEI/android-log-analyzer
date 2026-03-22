export class Registry {
    constructor() {
        this.services = new Map();
    }
    
    register(name, service) { this.services.set(name, service); }
    get(name) { return this.services.get(name); }
    has(name) { return this.services.has(name); }
    unregister(name) { this.services.delete(name); }
    clear() { this.services.clear(); }
}
