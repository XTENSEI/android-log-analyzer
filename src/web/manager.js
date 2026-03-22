export class Manager {
    constructor() {
        this.items = new Map();
    }
    
    add(id, item) { this.items.set(id, item); return this; }
    get(id) { return this.items.get(id); }
    has(id) { return this.items.has(id); }
    remove(id) { this.items.delete(id); return this; }
    clear() { this.items.clear(); return this; }
    forEach(fn) { this.items.forEach(fn); }
}
