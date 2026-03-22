import { createClient } from './client';

export class LogAnalyzerClient {
    constructor(baseUrl) {
        this.client = createClient(baseUrl);
    }

    async analyze(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await this.client.post('/analyze', formData);
        return response.data;
    }

    async getRules() {
        const response = await this.client.get('/rules');
        return response.data;
    }

    async health() {
        const response = await this.client.get('/health');
        return response.data;
    }
}

export default LogAnalyzerClient;
