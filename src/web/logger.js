export class Logger {
    static levels = { DEBUG: 0, INFO: 1, WARN: 2, ERROR: 3 };
    
    constructor(level = 'INFO') {
        this.level = Logger.levels[level];
    }
    
    debug(...args) { if (this.level <= 0) console.debug('[DEBUG]', ...args); }
    info(...args) { if (this.level <= 1) console.info('[INFO]', ...args); }
    warn(...args) { if (this.level <= 2) console.warn('[WARN]', ...args); }
    error(...args) { if (this.level <= 3) console.error('[ERROR]', ...args); }
}

export default Logger;
