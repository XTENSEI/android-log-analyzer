pub struct RingBuffer<T> {
    buffer: Vec<T>,
    capacity: usize,
    head: usize,
    tail: usize,
    full: bool,
}

impl<T> RingBuffer<T> {
    pub fn new(capacity: usize) -> Self {
        Self {
            buffer: Vec::with_capacity(capacity),
            capacity,
            head: 0,
            tail: 0,
            full: false,
        }
    }

    pub fn push(&mut self, item: T) {
        if self.full {
            self.buffer[self.tail] = item;
            self.tail = (self.tail + 1) % self.capacity;
            self.head = self.tail;
        } else {
            self.buffer.push(item);
            if self.buffer.len() == self.capacity {
                self.full = true;
            }
        }
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.buffer.is_empty() && !self.full {
            return None;
        }
        
        let item = self.buffer.remove(self.head);
        self.full = false;
        
        if !self.buffer.is_empty() {
            self.head = (self.head + 1) % self.capacity;
        }
        
        Some(item)
    }

    pub fn len(&self) -> usize {
        if self.full {
            self.capacity
        } else {
            self.buffer.len()
        }
    }

    pub fn is_empty(&self) -> bool {
        self.buffer.is_empty() && !self.full
    }
}
