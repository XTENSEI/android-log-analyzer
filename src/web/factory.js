export class Factory {
    constructor() {
        this.factories = {};
    }
    
    register(name, fn) { this.factories[name] = fn; }
    create(name, ...args) {
        const factory = this.factories[name];
        if (!factory) throw new Error(`Factory ${name} not found`);
        return factory(...args);
    }
}
