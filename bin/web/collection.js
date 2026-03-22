export class Collection extends Array {
    constructor(items = []) {
        super(...items);
    }
    
    first() { return this[0]; }
    last() { return this[this.length - 1]; }
    
    findBy(key, value) {
        return this.find(item => item[key] === value);
    }
    
    where(key, value) {
        return this.filter(item => item[key] === value);
    }
    
    pluck(key) {
        return this.map(item => item[key]);
    }
}
