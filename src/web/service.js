export class Service {
    constructor(baseURL) {
        this.client = baseURL;
    }
    
    async get(endpoint) {
        const res = await fetch(this.client + endpoint);
        return res.json();
    }
    
    async post(endpoint, data) {
        const res = await fetch(this.client + endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    }
}
