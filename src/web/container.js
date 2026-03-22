export class Container {
    constructor() {
        this.services = {};
    }
    
    register(name, fn) { this.services[name] = fn; }
    resolve(name) { 
        const Service = this.services[name];
        return new Service();
    }
    has(name) { return !!this.services[name]; }
}
