use crate::{LogEntry, LogLevel};
use memchr::memchr;
use std::io::{BufRead, Read};

pub struct LogParser {
    buffer: Vec<u8>,
    position: usize,
}

impl LogParser {
    pub fn new() -> Self {
        Self {
            buffer: Vec::with_capacity(65536),
            position: 0,
        }
    }

    pub fn parse_line(line: &str) -> Option<LogEntry> {
        let line = line.trim();
        if line.is_empty() {
            return None;
        }

        let parts: Vec<&str> = line.splitn(6, ' ').collect();
        if parts.len() < 5 {
            return None;
        }

        let timestamp = Self::parse_timestamp(parts[0]);
        let level = parts[1].chars().next().map(LogLevel::from).unwrap_or(LogLevel::Unknown);
        let tag = parts[2].to_string();
        let pid = parts[3].parse().unwrap_or(0);
        let tid = parts[4].parse().unwrap_or(0);
        let message = if parts.len() > 5 {
            parts[5..].join(" ")
        } else {
            String::new()
        };

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

    fn parse_timestamp(s: &str) -> i64 {
        if let Ok(ts) = s.parse::<i64>() {
            ts
        } else if s.contains('-') {
            0
        } else {
            0
        }
    }

    pub fn parse_stream<R: Read>(&mut self, reader: R, callback: impl Fn(LogEntry)) -> usize {
        let mut count = 0;
        let mut line_number = 0;

        for line in reader.lines() {
            line_number += 1;
            if let Ok(line) = line {
                if let Some(mut entry) = Self::parse_line(&line) {
                    entry.line_number = line_number;
                    callback(entry);
                    count += 1;
                }
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
