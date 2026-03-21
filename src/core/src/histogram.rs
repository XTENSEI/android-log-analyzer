use std::collections::HashMap;

pub struct Histogram {
    buckets: HashMap<String, usize>,
}

impl Histogram {
    pub fn new() -> Self {
        Self {
            buckets: HashMap::new(),
        }
    }

    pub fn record(&mut self, key: &str) {
        *self.buckets.entry(key.to_string()).or_insert(0) += 1;
    }

    pub fn get(&self, key: &str) -> usize {
        *self.buckets.get(key).unwrap_or(&0)
    }

    pub fn total(&self) -> usize {
        self.buckets.values().sum()
    }

    pub fn keys(&self) -> Vec<&String> {
        self.buckets.keys().collect()
    }
}

impl Default for Histogram {
    fn default() -> Self {
        Self::new()
    }
}
