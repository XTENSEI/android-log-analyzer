export class StringHelper {
    static capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    }
    
    static truncate(str, length) {
        return str.length > length ? str.slice(0, length) + '...' : str;
    }
    
    static slugify(str) {
        return str.toLowerCase().replace(/[^\w\s-]/g, '').replace(/[-\s]+/g, '-');
    }
    
    static template(str, data) {
        return str.replace(/\${(\w+)}/g, (_, k) => data[k] || '');
    }
}

export default StringHelper;
