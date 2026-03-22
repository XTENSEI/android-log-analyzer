export class Store {
    constructor() {
        this.state = {};
        this.listeners = [];
    }
    
    getState() { return this.state; }
    setState(state) { this.state = state; this.notify(); }
    subscribe(fn) { this.listeners.push(fn); return () => this.listeners = this.listeners.filter(l => l !== fn); }
    notify() { this.listeners.forEach(fn => fn(this.state)); }
}
