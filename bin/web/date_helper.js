export class DateHelper {
    static format(date, format = 'YYYY-MM-DD') {
        const d = new Date(date);
        return format
            .replace('YYYY', d.getFullYear())
            .replace('MM', String(d.getMonth() + 1).padStart(2, '0'))
            .replace('DD', String(d.getDate()).padStart(2, '0'))
            .replace('HH', String(d.getHours()).padStart(2, '0'))
            .replace('mm', String(d.getMinutes()).padStart(2, '0'));
    }
    
    static now() {
        return new Date();
    }
    
    static addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }
}

export default DateHelper;
