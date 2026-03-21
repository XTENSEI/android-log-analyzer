use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CacheEntry {
    pub key: String,
    pub value: String,
    pub ttl: u64,
}

pub struct Cache {
    entries: std::collections::HashMap<String, CacheEntry>,
}

impl Cache {
    pub fn new() -> Self {
        Self {
            entries: std::collections::HashMap::new(),
        }
    }

    pub fn set(&mut self, key: String, value: String, ttl: u64) {
        self.entries.insert(key, CacheEntry { key, value, ttl });
    }

    pub fn get(&self, key: &str) -> Option<String> {
        self.entries.get(key).map(|e| e.value.clone())
    }

    pub fn clear(&mut self) {
        self.entries.clear();
    }
}

impl Default for Cache {
    fn default() -> Self {
        Self::new()
    }
}
