export class StateMachine {
    constructor(initial) {
        this.state = initial;
        this.listeners = [];
    }
    
    transition(newState) {
        const oldState = this.state;
        this.state = newState;
        this.listeners.forEach(fn => fn(newState, oldState));
    }
    
    onTransition(fn) {
        this.listeners.push(fn);
        return () => {
            this.listeners = this.listeners.filter(l => l !== fn);
        };
    }
    
    getState() {
        return this.state;
    }
}

export default StateMachine;
