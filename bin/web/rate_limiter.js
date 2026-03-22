export class Debouncer {
    constructor(delay = 300) {
        this.delay = delay;
        this.timeout = null;
    }

    execute(callback) {
        if (this.timeout) {
            clearTimeout(this.timeout);
        }
        this.timeout = setTimeout(callback, this.delay);
    }

    cancel() {
        if (this.timeout) {
            clearTimeout(this.timeout);
        }
    }
}

export class Throttler {
    constructor(limit = 300) {
        this.limit = limit;
        this.lastRun = 0;
    }

    execute(callback) {
        const now = Date.now();
        if (now - this.lastRun >= this.limit) {
            this.lastRun = now;
            callback();
        }
    }
}

export default { Debouncer, Throttler };
