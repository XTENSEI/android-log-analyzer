export class FetchWrapper {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    
    async request(method, path, data) {
        const config = { method, headers: {} };
        if (data) {
            config.body = JSON.stringify(data);
            config.headers['Content-Type'] = 'application/json';
        }
        const res = await fetch(this.baseURL + path, config);
        return res.json();
    }
    
    get(path) { return this.request('GET', path); }
    post(path, data) { return this.request('POST', path, data); }
    put(path, data) { return this.request('PUT', path, data); }
    patch(path, data) { return this.request('PATCH', path, data); }
    delete(path) { return this.request('DELETE', path); }
}
