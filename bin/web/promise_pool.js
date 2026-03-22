export class PromisePool {
    constructor(concurrency) {
        this.concurrency = concurrency;
        this.running = 0;
        this.queue = [];
    }
    
    add(promise) {
        return new Promise((resolve, reject) => {
            this.queue.push({ promise, resolve, reject });
            this.process();
        });
    }
    
    async process() {
        if (this.running >= this.concurrency || this.queue.length === 0) return;
        
        this.running++;
        const { promise, resolve, reject } = this.queue.shift();
        
        try {
            const result = await promise;
            resolve(result);
        } catch (e) {
            reject(e);
        } finally {
            this.running--;
            this.process();
        }
    }
}

export default PromisePool;
