export class Controller {
    constructor() {
        this.actions = {};
    }
    
    action(name, fn) { this.actions[name] = fn; }
    execute(name, ...args) {
        const action = this.actions[name];
        if (!action) throw new Error(`Action ${name} not found`);
        return action(...args);
    }
}
