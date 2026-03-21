use crate::LogLevel;
use std::collections::HashMap;

#[derive(Debug, Default)]
pub struct LogStats {
    pub level_counts: HashMap<LogLevel, usize>,
    pub tag_counts: HashMap<String, usize>,
    pub pid_counts: HashMap<u32, usize>,
    pub total_bytes: usize,
    pub avg_line_length: f64,
}

impl LogStats {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn add_entry(&mut self, tag: &str, pid: u32, level: LogLevel, line_length: usize) {
        *self.level_counts.entry(level).or_insert(0) += 1;
        *self.tag_counts.entry(tag.to_string()).or_insert(0) += 1;
        *self.pid_counts.entry(pid).or_insert(0) += 1;
        self.total_bytes += line_length;
    }

    pub fn calculate_avg_line_length(&mut self, total_lines: usize) {
        if total_lines > 0 {
            self.avg_line_length = self.total_bytes as f64 / total_lines as f64;
        }
    }

    pub fn top_tags(&self, n: usize) -> Vec<(&str, usize)> {
        let mut tags: Vec<_> = self.tag_counts.iter()
            .map(|(k, v)| (k.as_str(), *v))
            .collect();
        tags.sort_by(|a, b| b.1.cmp(&a.1));
        tags.into_iter().take(n).collect()
    }

    pub fn top_processes(&self, n: usize) -> Vec<(u32, usize)> {
        let mut pids: Vec<_> = self.pid_counts.iter()
            .map(|(k, v)| (*k, *v))
            .collect();
        pids.sort_by(|a, b| b.1.cmp(&a.1));
        pids.into_iter().take(n).collect()
    }
}
