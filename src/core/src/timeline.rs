use crate::LogEntry;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TimelineEvent {
    pub timestamp: i64,
    pub event_type: EventType,
    pub tag: String,
    pub message: String,
    pub pid: u32,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EventType {
    Boot,
    AppStart,
    AppCrash,
    Anr,
    SystemError,
    NetworkError,
    MemoryIssue,
    Custom,
}

pub struct TimelineBuilder {
    events: Vec<TimelineEvent>,
    boot_time: Option<i64>,
}

impl TimelineBuilder {
    pub fn new() -> Self {
        Self {
            events: Vec::new(),
            boot_time: None,
        }
    }

    pub fn process_entry(&mut self, entry: &LogEntry) {
        if self.boot_time.is_none() {
            self.boot_time = Some(entry.timestamp);
        }

        let event_type = self.classify_entry(entry);
        
        self.events.push(TimelineEvent {
            timestamp: entry.timestamp,
            event_type,
            tag: entry.tag.clone(),
            message: entry.message.clone(),
            pid: entry.pid,
        });
    }

    fn classify_entry(&self, entry: &LogEntry) -> EventType {
        let msg = entry.message.to_lowercase();
        
        if msg.contains("boot") || msg.contains("init") {
            return EventType::Boot;
        }
        
        if msg.contains("anr") {
            return EventType::Anr;
        }
        
        if msg.contains("fatal") || msg.contains("crash") || msg.contains("died") {
            return EventType::AppCrash;
        }
        
        if msg.contains("network") || msg.contains("socket") || msg.contains("connection") {
            return EventType::NetworkError;
        }
        
        if msg.contains("memory") || msg.contains("oom") || msg.contains("low memory") {
            return EventType::MemoryIssue;
        }
        
        if msg.contains("error") || msg.contains("failed") {
            return EventType::SystemError;
        }
        
        EventType::Custom
    }

    pub fn build(self) -> Vec<TimelineEvent> {
        self.events
    }

    pub fn filter_by_type(&self, event_type: EventType) -> Vec<&TimelineEvent> {
        self.events
            .iter()
            .filter(|e| e.event_type == event_type)
            .collect()
    }

    pub fn get_boot_offset(&self, timestamp: i64) -> i64 {
        match self.boot_time {
            Some(boot) => timestamp - boot,
            None => 0,
        }
    }
}

impl Default for TimelineBuilder {
    fn default() -> Self {
        Self::new()
    }
}
