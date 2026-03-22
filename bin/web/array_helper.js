export class ArrayHelper {
    static unique(arr) {
        return [...new Set(arr)];
    }
    
    static chunk(arr, size) {
        return Array.from({ length: Math.ceil(arr.length / size) },
            (_, i) => arr.slice(i * size, i * size + size));
    }
    
    static shuffle(arr) {
        return arr.sort(() => Math.random() - 0.5);
    }
    
    static flatten(arr) {
        return arr.reduce((a, b) => a.concat(b), []);
    }
}

export default ArrayHelper;
