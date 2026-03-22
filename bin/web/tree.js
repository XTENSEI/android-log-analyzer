export class Tree {
    constructor(value) {
        this.value = value;
        this.children = [];
    }
    
    addChild(value) {
        const child = new Tree(value);
        this.children.push(child);
        return child;
    }
    
    traverse(fn) {
        fn(this.value);
        this.children.forEach(child => child.traverse(fn));
    }
    
    find(fn) {
        if (fn(this.value)) return this.value;
        for (const child of this.children) {
            const found = child.find(fn);
            if (found) return found;
        }
        return null;
    }
}

export default Tree;
