use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AggregatedStats {
    pub total_logs: usize,
    pub total_entries: usize,
    pub total_errors: usize,
    pub total_warnings: usize,
    pub log_files: Vec<LogFileInfo>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LogFileInfo {
    pub path: String,
    pub size_bytes: usize,
    pub entries: usize,
    pub errors: usize,
}

pub struct MultiLogAggregator {
    stats: AggregatedStats,
}

impl MultiLogAggregator {
    pub fn new() -> Self {
        Self {
            stats: AggregatedStats {
                total_logs: 0,
                total_entries: 0,
                total_errors: 0,
                total_warnings: 0,
                log_files: Vec::new(),
            },
        }
    }

    pub fn add_log(&mut self, path: &str, entries: usize, errors: usize, warnings: usize, size: usize) {
        self.stats.total_logs += 1;
        self.stats.total_entries += entries;
        self.stats.total_errors += errors;
        self.stats.total_warnings += warnings;
        
        self.stats.log_files.push(LogFileInfo {
            path: path.to_string(),
            size_bytes: size,
            entries,
            errors,
        });
    }

    pub fn build(self) -> AggregatedStats {
        self.stats
    }
}

impl Default for MultiLogAggregator {
    fn default() -> Self {
        Self::new()
    }
}
