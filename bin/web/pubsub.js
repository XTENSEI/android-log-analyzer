export class Publisher {
    constructor() {
        this.subscribers = {};
    }
    
    subscribe(topic, callback) {
        if (!this.subscribers[topic]) this.subscribers[topic] = [];
        this.subscribers[topic].push(callback);
    }
    
    publish(topic, data) {
        if (!this.subscribers[topic]) return;
        this.subscribers[topic].forEach(cb => cb(data));
    }
}

export default Publisher;
