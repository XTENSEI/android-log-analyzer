export class Validator {
    static validateFile(file) {
        const maxSize = 500 * 1024 * 1024;
        
        if (!file) {
            return { valid: false, error: 'No file selected' };
        }
        
        if (file.size > maxSize) {
            return { valid: false, error: 'File too large (max 500MB)' };
        }
        
        const allowedTypes = ['text/plain', 'application/octet-stream'];
        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(log|txt)$/i)) {
            return { valid: false, error: 'Invalid file type' };
        }
        
        return { valid: true };
    }

    static validateJSON(json) {
        try {
            JSON.parse(json);
            return { valid: true };
        } catch (e) {
            return { valid: false, error: 'Invalid JSON' };
        }
    }
}

export default Validator;
