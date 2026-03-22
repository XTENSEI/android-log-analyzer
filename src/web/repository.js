export class Repository {
    constructor(endpoint) {
        this.endpoint = endpoint;
    }
    
    async all() {
        const res = await fetch(this.endpoint);
        return res.json();
    }
    
    async find(id) {
        const res = await fetch(`${this.endpoint}/${id}`);
        return res.json();
    }
    
    async create(data) {
        const res = await fetch(this.endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    }
}
