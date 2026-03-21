use crate::{LogEntry, LogLevel};
use std::collections::HashSet;

#[derive(Debug, Clone)]
pub struct LogFilter {
    min_level: LogLevel,
    tags: Option<HashSet<String>>,
    pids: Option<HashSet<u32>>,
    search_text: Option<String>,
}

impl LogFilter {
    pub fn new() -> Self {
        Self {
            min_level: LogLevel::Verbose,
            tags: None,
            pids: None,
            search_text: None,
        }
    }

    pub fn with_min_level(mut self, level: LogLevel) -> Self {
        self.min_level = level;
        self
    }

    pub fn with_tags(mut self, tags: Vec<String>) -> Self {
        self.tags = Some(tags.into_iter().collect());
        self
    }

    pub fn with_pids(mut self, pids: Vec<u32>) -> Self {
        self.pids = Some(pids.into_iter().collect());
        self
    }

    pub fn with_search(mut self, text: String) -> Self {
        self.search_text = Some(text);
        self
    }

    pub fn matches(&self, entry: &LogEntry) -> bool {
        if entry.level < self.min_level {
            return false;
        }

        if let Some(ref tags) = self.tags {
            if !tags.contains(&entry.tag) {
                return false;
            }
        }

        if let Some(ref pids) = self.pids {
            if !pids.contains(&entry.pid) {
                return false;
            }
        }

        if let Some(ref search) = self.search_text {
            let msg = entry.message.to_lowercase();
            let search_lower = search.to_lowercase();
            if !msg.contains(&search_lower) && !entry.tag.to_lowercase().contains(&search_lower) {
                return false;
            }
        }

        true
    }
}

impl Default for LogFilter {
    fn default() -> Self {
        Self::new()
    }
}
