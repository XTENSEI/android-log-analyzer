export class Maybe {
    constructor(value) {
        this.value = value;
    }
    
    static of(value) {
        return new Maybe(value);
    }
    
    static nothing() {
        return new Maybe(null);
    }
    
    isNothing() {
        return this.value === null || this.value === undefined;
    }
    
    map(fn) {
        if (this.isNothing()) return this;
        return Maybe.of(fn(this.value));
    }
    
    getOrElse(defaultValue) {
        return this.isNothing() ? defaultValue : this.value;
    }
}

export default Maybe;
