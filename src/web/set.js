export class Set {
    constructor() {
        this.items = [];
    }
    
    add(item) {
        if (!this.has(item)) {
            this.items.push(item);
        }
    }
    
    has(item) {
        return this.items.includes(item);
    }
    
    delete(item) {
        const index = this.items.indexOf(item);
        if (index > -1) {
            this.items.splice(index, 1);
        }
    }
    
    size() {
        return this.items.length;
    }
    
    values() {
        return [...this.items];
    }
}

export default Set;
