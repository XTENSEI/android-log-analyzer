export class Graph {
    constructor() {
        this.nodes = new Map();
    }
    
    addNode(value) {
        if (!this.nodes.has(value)) {
            this.nodes.set(value, []);
        }
    }
    
    addEdge(from, to) {
        this.addNode(from);
        this.addNode(to);
        this.nodes.get(from).push(to);
    }
    
    getNeighbors(node) {
        return this.nodes.get(node) || [];
    }
    
    bfs(start, visit) {
        const visited = new Set();
        const queue = [start];
        
        while (queue.length) {
            const node = queue.shift();
            if (visited.has(node)) continue;
            
            visited.add(node);
            visit(node);
            queue.push(...this.getNeighbors(node));
        }
    }
}

export default Graph;
