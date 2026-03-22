export class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'dark';
    }

    init() {
        this.apply(this.theme);
    }

    toggle() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        this.apply(this.theme);
        localStorage.setItem('theme', this.theme);
    }

    apply(theme) {
        document.body.className = theme;
    }

    isDark() {
        return this.theme === 'dark';
    }
}

export default ThemeManager;
