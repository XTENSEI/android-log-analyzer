export class ObjectHelper {
    static clone(obj) {
        return JSON.parse(JSON.stringify(obj));
    }
    
    static merge(a, b) {
        return { ...a, ...b };
    }
    
    static pick(obj, keys) {
        return keys.reduce((acc, key) => {
            if (key in obj) acc[key] = obj[key];
            return acc;
        }, {});
    }
    
    static omit(obj, keys) {
        return Object.keys(obj).filter(k => !keys.includes(k))
            .reduce((acc, k) => { acc[k] = obj[k]; return acc; }, {});
    }
}

export default ObjectHelper;
