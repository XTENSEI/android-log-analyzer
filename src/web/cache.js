export class LocalCache {
    constructor(prefix = 'cache_') {
        this.prefix = prefix;
    }

    set(key, value, ttl = 36000) {
        const item = {
            value,
            expires: Date.now() + ttl
        };
        localStorage.setItem(this.prefix + key, JSON.stringify(item));
    }

    get(key) {
        const item = localStorage.getItem(this.prefix + key);
        if (!item) return null;
        
        const data = JSON.parse(item);
        if (Date.now() > data.expires) {
            this.remove(key);
            return null;
        }
        return data.value;
    }

    remove(key) {
        localStorage.removeItem(this.prefix + key);
    }

    clear() {
        Object.keys(localStorage)
            .filter(k => k.startsWith(this.prefix))
            .forEach(k => localStorage.removeItem(k));
    }
}

export default LocalCache;
