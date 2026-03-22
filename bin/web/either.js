export class Either {
    constructor(value, isLeft) {
        this.value = value;
        this.isLeft = isLeft;
    }
    
    static left(value) {
        return new Either(value, true);
    }
    
    static right(value) {
        return new Either(value, false);
    }
    
    isRight() {
        return !this.isLeft;
    }
    
    map(fn) {
        return this.isLeft ? this : Either.right(fn(this.value));
    }
}

export default Either;
