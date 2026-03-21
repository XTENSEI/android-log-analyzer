use std::collections::HashMap;

pub struct TimeSeries {
    data: HashMap<i64, usize>,
    interval_ms: i64,
}

impl TimeSeries {
    pub fn new(interval_ms: i64) -> Self {
        Self {
            data: HashMap::new(),
            interval_ms,
        }
    }

    pub fn add(&mut self, timestamp: i64) {
        let bucket = (timestamp / self.interval_ms) * self.interval_ms;
        *self.data.entry(bucket).or_insert(0) += 1;
    }

    pub fn get_buckets(&self) -> Vec<(i64, usize)> {
        let mut buckets: Vec<_> = self.data.iter().map(|(k, v)| (*k, *v)).collect();
        buckets.sort_by_key(|(k, _)| *k);
        buckets
    }

    pub fn peak(&self) -> Option<(i64, usize)> {
        self.data.iter().max_by_key(|(_, v)| *v).map(|(k, v)| (*k, *v))
    }
}
