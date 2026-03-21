use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessInfo {
    pub pid: u32,
    pub name: Option<String>,
    pub tag_count: usize,
    pub error_count: usize,
    pub warning_count: usize,
}

pub struct ProcessTracker {
    processes: std::collections::HashMap<u32, ProcessInfo>,
}

impl ProcessTracker {
    pub fn new() -> Self {
        Self {
            processes: std::collections::HashMap::new(),
        }
    }

    pub fn track(&mut self, pid: u32, tag: &str, is_error: bool, is_warning: bool) {
        let info = self.processes.entry(pid).or_insert(ProcessInfo {
            pid,
            name: None,
            tag_count: 0,
            error_count: 0,
            warning_count: 0,
        });
        
        info.tag_count += 1;
        if is_error { info.error_count += 1; }
        if is_warning { info.warning_count += 1; }
    }

    pub fn get_process(&self, pid: u32) -> Option<&ProcessInfo> {
        self.processes.get(&pid)
    }

    pub fn all_processes(&self) -> Vec<&ProcessInfo> {
        self.processes.values().collect()
    }
}

impl Default for ProcessTracker {
    fn default() -> Self {
        Self::new()
    }
}
