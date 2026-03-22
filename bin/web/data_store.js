export class DataStore {
    constructor() {
        this.store = new Map();
    }
    
    set(key, value) { this.store.set(key, value); return this; }
    get(key) { return this.store.get(key); }
    has(key) { return this.store.has(key); }
    delete(key) { this.store.delete(key); return this; }
    clear() { this.store.clear(); return this; }
    keys() { return Array.from(this.store.keys()); }
    values() { return Array.from(this.store.values()); }
    entries() { return Array.from(this.store.entries()); }
}
