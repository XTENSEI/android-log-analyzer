use std::collections::HashMap;

pub struct TagIndex {
    tags: HashMap<String, Vec<usize>>,
}

impl TagIndex {
    pub fn new() -> Self {
        Self {
            tags: HashMap::new(),
        }
    }

    pub fn add(&mut self, tag: &str, line_number: usize) {
        self.tags.entry(tag.to_string()).or_insert_with(Vec::new).push(line_number);
    }

    pub fn get_lines(&self, tag: &str) -> Option<&Vec<usize>> {
        self.tags.get(tag)
    }

    pub fn all_tags(&self) -> Vec<&String> {
        self.tags.keys().collect()
    }
}

impl Default for TagIndex {
    fn default() -> Self {
        Self::new()
    }
}
