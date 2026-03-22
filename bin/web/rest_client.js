export class RESTClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    
    async fetch(method, path, body = null) {
        const options = { method, headers: { 'Content-Type': 'application/json' } };
        if (body) options.body = JSON.stringify(body);
        const response = await fetch(this.baseURL + path, options);
        return response.json();
    }
    
    get(path) { return this.fetch('GET', path); }
    post(path, body) { return this.fetch('POST', path, body); }
    put(path, body) { return this.fetch('PUT', path, body); }
    delete(path) { return this.fetch('DELETE', path); }
}
