export class Uploader {
    constructor() {
        this.file = null;
        this.progress = 0;
    }

    setFile(file) {
        this.file = file;
    }

    async upload(onProgress) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            const formData = new FormData();
            
            formData.append('file', this.file);
            
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    this.progress = (e.loaded / e.total) * 100;
                    onProgress(this.progress);
                }
            });
            
            xhr.addEventListener('load', () => {
                resolve(xhr.response);
            });
            
            xhr.addEventListener('error', reject);
            
            xhr.open('POST', '/analyze');
            xhr.send(formData);
        });
    }
}

export default Uploader;
