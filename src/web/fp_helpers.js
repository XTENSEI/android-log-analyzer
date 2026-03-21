export function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        }
        return (...more) => curried(...args, ...more);
    };
}

export function compose(...fns) {
    return x => fns.reduceRight((v, f) => f(v), x);
}

export function pipe(x, ...fns) {
    return fns.reduce((v, f) => f(v), x);
}
