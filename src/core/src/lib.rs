use serde::{Deserialize, Serialize};
use std::fmt;

pub mod analyzer;
pub mod config;
pub mod correlation;
pub mod parser;
pub mod rules;

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
