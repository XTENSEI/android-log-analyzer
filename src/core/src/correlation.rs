use crate::{LogEntry, LogLevel};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

pub struct LogCorrelator {
    entries_by_pid: HashMap<u32, Vec<LogEntry>>,
    entries_by_time: Vec<LogEntry>,
    entries_by_tag: HashMap<String, Vec<LogEntry>>,
}

impl LogCorrelator {
    pub fn new() -> Self {
        Self {
            entries_by_pid: HashMap::new(),
            entries_by_time: Vec::new(),
            entries_by_tag: HashMap::new(),
        }
    }

    pub fn load_log<P: AsRef<Path>>(&mut self, path: P) -> Result<usize, String> {
        let file = File::open(path).map_err(|e| e.to_string())?;
        let reader = BufReader::new(file);
        
        let mut count = 0;
        
        for line in reader.lines() {
            if let Ok(line) = line {
                if let Some(entry) = crate::parser::LogParser::parse_line(&line) {
                    let mut e = entry;
                    e.line_number = count + 1;
                    
                    self.entries_by_pid.entry(e.pid).or_insert_with(Vec::new).push(e.clone());
                    self.entries_by_time.push(e.clone());
                    self.entries_by_tag.entry(e.tag.clone()).or_insert_with(Vec::new).push(e);
                    
                    count += 1;
                }
            }
        }
        
        self.entries_by_time.sort_by_key(|e| e.timestamp);
        
        Ok(count)
    }

    pub fn find_related_by_pid(&self, pid: u32) -> &[LogEntry] {
        self.entries_by_pid.get(&pid).map(|v| v.as_slice()).unwrap_or(&[])
    }

    pub fn find_errors_near(&self, target_line: usize, window: usize) -> Vec<&LogEntry> {
        let start = target_line.saturating_sub(window);
        let end = (target_line + window).min(self.entries_by_time.len());
        
        self.entries_by_time[start..end]
            .iter()
            .filter(|e| e.level == LogLevel::Error || e.level == LogLevel::Fatal)
            .collect()
    }

    pub fn find_crashes(&self) -> Vec<&LogEntry> {
        self.entries_by_time
            .iter()
            .filter(|e| {
                let msg = e.message.to_lowercase();
                msg.contains("fatal exception") || 
                msg.contains("crash") || 
                msg.contains("died")
            })
            .collect()
    }

    pub fn get_process_summary(&self) -> HashMap<u32, ProcessInfo> {
        let mut summary: HashMap<u32, ProcessInfo> = HashMap::new();
        
        for (pid, entries) in &self.entries_by_pid {
            let error_count = entries.iter().filter(|e| e.level == LogLevel::Error).count();
            let warning_count = entries.iter().filter(|e| e.level == LogLevel::Warning).count();
            let tag_count = entries.iter().map(|e| e.tag.clone()).collect::<std::collections::HashSet<_>>().len();
            
            summary.insert(*pid, ProcessInfo {
                pid: *pid,
                entry_count: entries.len(),
                error_count,
                warning_count,
                unique_tags: tag_count,
            });
        }
        
        summary
    }
}

impl Default for LogCorrelator {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Debug, Clone)]
pub struct ProcessInfo {
    pub pid: u32,
    pub entry_count: usize,
    pub error_count: usize,
    pub warning_count: usize,
    pub unique_tags: usize,
}
