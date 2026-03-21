export class Paginator {
    constructor(items, perPage = 10) {
        this.items = items;
        this.perPage = perPage;
        this.currentPage = 1;
    }

    getPage(page) {
        const start = (page - 1) * this.perPage;
        const end = start + this.perPage;
        return {
            items: this.items.slice(start, end),
            page,
            totalPages: Math.ceil(this.items.length / this.perPage),
            totalItems: this.items.length
        };
    }

    get current() {
        return this.getPage(this.currentPage);
    }
}

export default Paginator;
