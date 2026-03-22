export class IOC {
    constructor() {
        this.bindings = new Map();
    }
    
    bind(key, implementation) {
        this.bindings.set(key, implementation);
    }
    
    resolve(key) {
        const binding = this.bindings.get(key);
        if (!binding) throw new Error(`No binding for ${key}`);
        return typeof binding === 'function' ? new binding() : binding;
    }
}
