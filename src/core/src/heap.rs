pub struct MinHeap<T: Ord> {
    data: Vec<T>,
}

impl<T: Ord> MinHeap<T> {
    pub fn new() -> Self {
        Self { data: Vec::new() }
    }

    pub fn push(&mut self, item: T) {
        self.data.push(item);
        self.bubble_up(self.data.len() - 1);
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.data.is_empty() {
            return None;
        }
        let result = self.data.remove(0);
        if !self.data.is_empty() {
            let last = self.data.remove(self.data.len() - 1);
            self.data.insert(0, last);
            self.bubble_down(0);
        }
        Some(result)
    }

    fn bubble_up(&mut self, mut i: usize) {
        while i > 0 {
            let parent = (i - 1) / 2;
            if self.data[i] < self.data[parent] {
                self.data.swap(i, parent);
                i = parent;
            } else {
                break;
            }
        }
    }

    fn bubble_down(&mut self, mut i: usize) {
        loop {
            let left = 2 * i + 1;
            let right = 2 * i + 2;
            let mut smallest = i;
            
            if left < self.data.len() && self.data[left] < self.data[smallest] {
                smallest = left;
            }
            if right < self.data.len() && self.data[right] < self.data[smallest] {
                smallest = right;
            }
            
            if smallest != i {
                self.data.swap(i, smallest);
                i = smallest;
            } else {
                break;
            }
        }
    }
}

impl<T: Ord> Default for MinHeap<T> {
    fn default() -> Self {
        Self::new()
    }
}
