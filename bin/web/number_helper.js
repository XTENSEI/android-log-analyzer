export class NumberHelper {
    static format(num, decimals = 0) {
        return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
    
    static random(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    static clamp(num, min, max) {
        return Math.min(Math.max(num, min), max);
    }
}

export default NumberHelper;
