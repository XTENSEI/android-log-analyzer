export class SearchFilter {
    constructor(items) {
        this.items = items;
    }

    search(query, fields) {
        if (!query) return this.items;
        
        const lowerQuery = query.toLowerCase();
        
        return this.items.filter(item => {
            return fields.some(field => {
                const value = item[field];
                return value && value.toString().toLowerCase().includes(lowerQuery);
            });
        });
    }

    filter(predicate) {
        return this.items.filter(predicate);
    }

    sort(field, direction = 'asc') {
        const sorted = [...this.items];
        sorted.sort((a, b) => {
            const aVal = a[field];
            const bVal = b[field];
            if (aVal < bVal) return direction === 'asc' ? -1 : 1;
            if (aVal > bVal) return direction === 'asc' ? 1 : -1;
            return 0;
        });
        return sorted;
    }
}

export default SearchFilter;
