use crate::{LogEntry, LogLevel};

pub struct LogExporter;

impl LogExporter {
    pub fn export_csv(entries: &[LogEntry], output: &str) -> Result<(), String> {
        let mut content = String::from("timestamp,level,tag,pid,tid,message,line_number\n");
        
        for entry in entries {
            let message = entry.message.replace(",", ";").replace("\n", " ");
            content.push_str(&format!(
                "{},{:?},{},{},{},\"{}\",{}\n",
                entry.timestamp, entry.level, entry.tag, entry.pid, entry.tid, message, entry.line_number
            ));
        }
        
        std::fs::write(output, content).map_err(|e| e.to_string())
    }

    pub fn export_text(entries: &[LogEntry], output: &str) -> Result<(), String> {
        let mut content = String::new();
        
        for entry in entries {
            content.push_str(&format!(
                "{:?} {} {} {}: {}\n",
                entry.timestamp, entry.level, entry.tag, entry.pid, entry.message
            ));
        }
        
        std::fs::write(output, content).map_err(|e| e.to_string())
    }

    pub fn filter_entries(entries: &[LogEntry], min_level: LogLevel) -> Vec<&LogEntry> {
        entries
            .iter()
            .filter(|e| e.level >= min_level)
            .collect()
    }

    pub fn filter_by_tag(entries: &[LogEntry], tag: &str) -> Vec<&LogEntry> {
        entries
            .iter()
            .filter(|e| e.tag == tag)
            .collect()
    }

    pub fn filter_by_pid(entries: &[LogEntry], pid: u32) -> Vec<&LogEntry> {
        entries
            .iter()
            .filter(|e| e.pid == pid)
            .collect()
    }

    pub fn search(entries: &[LogEntry], query: &str) -> Vec<&LogEntry> {
        let query_lower = query.to_lowercase();
        entries
            .iter()
            .filter(|e| {
                e.message.to_lowercase().contains(&query_lower) ||
                e.tag.to_lowercase().contains(&query_lower)
            })
            .collect()
    }
}
