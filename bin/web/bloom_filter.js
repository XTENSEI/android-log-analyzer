export class BloomFilter {
    constructor(size = 1000) {
        this.size = size;
        this.filter = new Array(size).fill(false);
    }
    
    hash(str, seed = 0) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = (hash * 31 + str.charCodeAt(i) + seed) % this.size;
        }
        return hash;
    }
    
    add(item) {
        for (let i = 0; i < 3; i++) {
            this.filter[this.hash(item, i)] = true;
        }
    }
    
    has(item) {
        for (let i = 0; i < 3; i++) {
            if (!this.filter[this.hash(item, i)]) return false;
        }
        return true;
    }
}

export default BloomFilter;
