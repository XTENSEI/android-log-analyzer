export class BloomFilter {
    constructor(size = 100, hashes = 3) {
        this.size = size;
        this.hashes = hashes;
        this.filter = new Array(size).fill(false);
    }
    
    hash(str, seed) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = (hash * 31 + str.charCodeAt(i) + seed) % this.size;
        }
        return hash;
    }
    
    add(item) {
        for (let i = 0; i < this.hashes; i++) {
            this.filter[this.hash(item, i)] = true;
        }
    }
    
    test(item) {
        for (let i = 0; i < this.hashes; i++) {
            if (!this.filter[this.hash(item, i)]) return false;
        }
        return true;
    }
}

export default BloomFilter;
