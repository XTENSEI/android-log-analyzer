use std::collections::HashMap;

pub struct PidIndex {
    entries_by_pid: HashMap<u32, Vec<u32>>,
}

impl PidIndex {
    pub fn new() -> Self {
        Self {
            entries_by_pid: HashMap::new(),
        }
    }

    pub fn add(&mut self, pid: u32, tid: u32) {
        self.entries_by_pid.entry(pid).or_insert_with(Vec::new).push(tid);
    }

    pub fn get_tids(&self, pid: u32) -> Option<&Vec<u32>> {
        self.entries_by_pid.get(&pid)
    }
}

impl Default for PidIndex {
    fn default() -> Self {
        Self::new()
    }
}
