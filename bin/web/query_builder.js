export class QueryBuilder {
    constructor() {
        this.params = new URLSearchParams();
    }

    add(key, value) {
        this.params.append(key, value);
        return this;
    }

    set(key, value) {
        this.params.set(key, value);
        return this;
    }

    get(key) {
        return this.params.get(key);
    }

    delete(key) {
        this.params.delete(key);
        return this;
    }

    toString() {
        return this.params.toString();
    }

    toURL(base) {
        return `${base}?${this.toString()}`;
    }
}

export default QueryBuilder;
