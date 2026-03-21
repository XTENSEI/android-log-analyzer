use std::collections::HashMap;

pub struct ErrorAggregator {
    error_messages: HashMap<String, usize>,
}

impl ErrorAggregator {
    pub fn new() -> Self {
        Self {
            error_messages: HashMap::new(),
        }
    }

    pub fn add_error(&mut self, message: &str) {
        *self.error_messages.entry(message.to_string()).or_insert(0) += 1;
    }

    pub fn top_errors(&self, n: usize) -> Vec<(&String, &usize)> {
        let mut errors: Vec<_> = self.error_messages.iter().collect();
        errors.sort_by(|a, b| b.1.cmp(a.1));
        errors.into_iter().take(n).collect()
    }

    pub fn total_unique(&self) -> usize {
        self.error_messages.len()
    }
}

impl Default for ErrorAggregator {
    fn default() -> Self {
        Self::new()
    }
}
