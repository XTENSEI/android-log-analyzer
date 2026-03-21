use std::collections::HashSet;

pub struct Deduplicator {
    seen: HashSet<String>,
}

impl Deduplicator {
    pub fn new() -> Self {
        Self {
            seen: HashSet::new(),
        }
    }

    pub fn add(&mut self, key: &str) -> bool {
        self.seen.insert(key.to_string())
    }

    pub fn is_new(&self, key: &str) -> bool {
        !self.seen.contains(key)
    }

    pub fn clear(&mut self) {
        self.seen.clear();
    }

    pub fn count(&self) -> usize {
        self.seen.len()
    }
}

impl Default for Deduplicator {
    fn default() -> Self {
        Self::new()
    }
}
