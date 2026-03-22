export class Observable {
    constructor() {
        this.observers = new Map();
    }
    
    subscribe(event, fn) {
        if (!this.observers.has(event)) {
            this.observers.set(event, new Set());
        }
        this.observers.get(event).add(fn);
        return () => this.unsubscribe(event, fn);
    }
    
    unsubscribe(event, fn) {
        if (this.observers.has(event)) {
            this.observers.get(event).delete(fn);
        }
    }
    
    emit(event, data) {
        if (this.observers.has(event)) {
            this.observers.get(event).forEach(fn => fn(data));
        }
    }
}

export default Observable;
