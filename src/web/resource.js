export class Resource {
    constructor(client, path) {
        this.client = client;
        this.path = path;
    }
    
    list() { return this.client.get(this.path); }
    get(id) { return this.client.get(`${this.path}/${id}`); }
    create(data) { return this.client.post(this.path, data); }
    update(id, data) { return this.client.put(`${this.path}/${id}`, data); }
    remove(id) { return this.client.delete(`${this.path}/${id}`); }
}
