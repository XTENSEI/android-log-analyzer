export class HTTPClient {
    async get(url) {
        const res = await fetch(url);
        return res.json();
    }
    
    async post(url, data) {
        const res = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        return res.json();
    }
}
