export class URLHelper {
    static parse(url) {
        return new URL(url);
    }
    
    static build(base, params) {
        const url = new URL(base);
        Object.entries(params).forEach(([k, v]) => url.searchParams.append(k, v));
        return url.toString();
    }
    
    static getParam(name) {
        return new URLSearchParams(window.location.search).get(name);
    }
}

export default URLHelper;
