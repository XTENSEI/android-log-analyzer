use std::collections::HashMap;

pub struct RateLimiter {
    requests: HashMap<String, usize>,
    window_ms: u64,
    max_requests: usize,
}

impl RateLimiter {
    pub fn new(window_ms: u64, max_requests: usize) -> Self {
        Self {
            requests: HashMap::new(),
            window_ms,
            max_requests,
        }
    }

    pub fn allow(&mut self, key: &str) -> bool {
        let count = self.requests.entry(key.to_string()).or_insert(0);
        *count += 1;
        *count <= self.max_requests
    }

    pub fn reset(&mut self, key: &str) {
        self.requests.remove(key);
    }
}
