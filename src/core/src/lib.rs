use serde::{Deserialize, Serialize};
use std::fmt;

pub mod aggregator;
pub mod analyzer;
pub mod atomic;
pub mod bitset;
pub mod bloom;
pub mod cache;
pub mod config;
pub mod correlation;
pub mod counter;
pub mod dedup;
pub mod error_agg;
pub mod export;
pub mod filter;
pub mod heap;
pub mod histogram;
pub mod index;
pub mod logger;
pub mod lru_cache;
pub mod mmap;
pub mod parser;
pub mod performance;
pub mod pid_index;
pub mod priority;
pub mod process;
pub mod ratelimit;
pub mod reporter;
pub mod ring;
pub mod rules;
pub mod scorer;
pub mod sparse;
pub mod stats;
pub mod timeline;
pub mod timer;
pub mod timeseries;
pub mod trie;
pub mod watcher;
pub mod window;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LogEntry {
    pub timestamp: i64,
    pub level: LogLevel,
    pub tag: String,
    pub pid: u32,
    pub tid: u32,
    pub message: String,
    pub line_number: usize,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum LogLevel {
    Verbose,
    Debug,
    Info,
    Warning,
    Error,
    Fatal,
    Unknown,
}

impl fmt::Display for LogLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LogLevel::Verbose => write!(f, "V"),
            LogLevel::Debug => write!(f, "D"),
            LogLevel::Info => write!(f, "I"),
            LogLevel::Warning => write!(f, "W"),
            LogLevel::Error => write!(f, "E"),
            LogLevel::Fatal => write!(f, "F"),
            LogLevel::Unknown => write!(f, "?"),
        }
    }
}

impl From<char> for LogLevel {
    fn from(c: char) -> Self {
        match c {
            'V' => LogLevel::Verbose,
            'D' => LogLevel::Debug,
            'I' => LogLevel::Info,
            'W' => LogLevel::Warning,
            'E' => LogLevel::Error,
            'F' => LogLevel::Fatal,
            _ => LogLevel::Unknown,
        }
    }
}
