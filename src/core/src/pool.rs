pub struct Pool<T> {
    items: Vec<T>,
    available: Vec<bool>,
}

impl<T: Default> Pool<T> {
    pub fn new(capacity: usize) -> Self {
        let items = (0..capacity).map(|_| T::default()).collect();
        let available = vec![true; capacity];
        
        Self { items, available }
    }

    pub fn acquire(&mut self) -> Option<&mut T> {
        for (i, available) in self.available.iter_mut().enumerate() {
            if *available {
                *available = false;
                return self.items.get_mut(i);
            }
        }
        None
    }

    pub fn release(&mut self, index: usize) {
        if index < self.available.len() {
            self.available[index] = true;
        }
    }
}
