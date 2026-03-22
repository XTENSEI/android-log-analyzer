export class Model {
    constructor(data = {}) {
        Object.assign(this, data);
    }
    
    save() {
        return this.id ? this.update() : this.create();
    }
    
    create() { return Promise.resolve(this); }
    update() { return Promise.resolve(this); }
    delete() { return Promise.resolve(true); }
    
    toJSON() { return { ...this }; }
}
