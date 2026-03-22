export class Action {
    constructor(name, handler) {
        this.name = name;
        this.handler = handler;
    }
    
    execute(...args) { return this.handler(...args); }
}
