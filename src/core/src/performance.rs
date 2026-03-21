use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PerformanceMetrics {
    pub entries_per_second: f64,
    pub mb_per_second: f64,
    pub avg_line_parse_time_us: f64,
    pub memory_usage_mb: f64,
    pub peak_memory_mb: f64,
}

impl PerformanceMetrics {
    pub fn new(entries: usize, bytes: usize, time_ms: u64, memory_kb: u64) -> Self {
        let time_s = time_ms as f64 / 1000.0;
        
        Self {
            entries_per_second: if time_s > 0.0 { entries as f64 / time_s } else { 0.0 },
            mb_per_second: if time_s > 0.0 { (bytes as f64 / 1_048_576.0) / time_s } else { 0.0 },
            avg_line_parse_time_us: if entries > 0 { (time_ms * 1000) as f64 / entries as f64 } else { 0.0 },
            memory_usage_mb: memory_kb as f64 / 1024.0,
            peak_memory_mb: memory_kb as f64 / 1024.0,
        }
    }

    pub fn summary(&self) -> String {
        format!(
            "Performance: {:.0} entries/s, {:.1} MB/s, {:.2} µs/line, {:.1} MB memory",
            self.entries_per_second,
            self.mb_per_second,
            self.avg_line_parse_time_us,
            self.memory_usage_mb
        )
    }
}
