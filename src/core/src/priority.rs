pub struct PriorityQueue<T> {
    items: Vec<T>,
    priorities: Vec<i32>,
}

impl<T> PriorityQueue<T> {
    pub fn new() -> Self {
        Self {
            items: Vec::new(),
            priorities: Vec::new(),
        }
    }

    pub fn push(&mut self, item: T, priority: i32) {
        self.items.push(item);
        self.priorities.push(priority);
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.items.is_empty() {
            return None;
        }
        
        let mut max_idx = 0;
        for i in 1..self.priorities.len() {
            if self.priorities[i] > self.priorities[max_idx] {
                max_idx = i;
            }
        }
        
        self.priorities.remove(max_idx);
        Some(self.items.remove(max_idx))
    }

    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }

    pub fn len(&self) -> usize {
        self.items.len()
    }
}

impl<T> Default for PriorityQueue<T> {
    fn default() -> Self {
        Self::new()
    }
}
