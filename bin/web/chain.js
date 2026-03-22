export class Chain {
    constructor(value) {
        this.value = value;
    }
    
    map(fn) {
        return new Chain(fn(this.value));
    }
    
    flatMap(fn) {
        return fn(this.value);
    }
    
    get() {
        return this.value;
    }
}

export default Chain;
