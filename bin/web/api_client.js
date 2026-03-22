export class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    
    async request(method, endpoint, data) {
        const url = this.baseURL + endpoint;
        const options = { method, headers: { 'Content-Type': 'application/json' } };
        if (data) options.body = JSON.stringify(data);
        const res = await fetch(url, options);
        return res.json();
    }
    
    get(endpoint) { return this.request('GET', endpoint); }
    post(endpoint, data) { return this.request('POST', endpoint, data); }
    put(endpoint, data) { return this.request('PUT', endpoint, data); }
    delete(endpoint) { return this.request('DELETE', endpoint); }
}
