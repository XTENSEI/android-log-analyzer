use crate::{LogEntry, LogLevel};
use std::io::BufRead;

pub struct LogParser {
    _buffer: Vec<u8>,
    _position: usize,
}

impl LogParser {
    pub fn new() -> Self {
        Self {
            _buffer: Vec::with_capacity(65536),
            _position: 0,
        }
    }

    pub fn parse_line(line: &str) -> Option<LogEntry> {
        let line = line.trim();
        if line.is_empty() {
            return None;
        }

        let parts: Vec<&str> = line.split(' ').filter(|s| !s.is_empty()).collect();
        if parts.len() < 6 {
            return None;
        }

        let month_day = parts[0];
        let time = parts[1];
        let pid_str = parts[2];
        let tid_str = parts[3];
        let level_char = parts[4].chars().next().unwrap_or('?');
        let level = LogLevel::from(level_char);
        let tag_with_colon = parts[5];
        let tag = tag_with_colon.trim_end_matches(':').to_string();
        let message = if parts.len() > 6 {
            parts[6..].join(" ")
        } else {
            String::new()
        };

        let timestamp = Self::parse_timestamp(month_day, time);
        let pid = pid_str.parse().unwrap_or(0);
        let tid = tid_str.parse().unwrap_or(0);

        Some(LogEntry {
            timestamp,
            level,
            tag,
            pid,
            tid,
            message,
            line_number: 0,
        })
    }

    fn parse_timestamp(month_day: &str, time: &str) -> i64 {
        let combined = format!("{} {}", month_day, time);
        if let Ok(dt) = chrono::NaiveDateTime::parse_from_str(&combined, "%m-%d %H:%M:%S%.f") {
            dt.and_utc().timestamp()
        } else {
            0
        }
    }

    pub fn parse_stream<R: BufRead>(&mut self, mut reader: R, callback: impl Fn(LogEntry)) -> usize {
        let mut count = 0;
        let mut line_number = 0;
        let mut line = String::new();

        loop {
            line.clear();
            match reader.read_line(&mut line) {
                Ok(0) => break,
                Ok(_) => {
                    line_number += 1;
                    if let Some(mut entry) = Self::parse_line(&line) {
                        entry.line_number = line_number;
                        callback(entry);
                        count += 1;
                    }
                }
                Err(_) => break,
            }
        }

        count
    }
}

impl Default for LogParser {
    fn default() -> Self {
        Self::new()
    }
}
