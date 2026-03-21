use std::collections::HashMap;

pub struct SparseArray<T: Default> {
    data: HashMap<usize, T>,
    default: T,
}

impl<T: Default + Clone> SparseArray<T> {
    pub fn new() -> Self {
        Self {
            data: HashMap::new(),
            default: T::default(),
        }
    }

    pub fn with_default(default: T) -> Self {
        Self {
            data: HashMap::new(),
            default,
        }
    }

    pub fn set(&mut self, index: usize, value: T) {
        self.data.insert(index, value);
    }

    pub fn get(&self, index: usize) -> &T {
        self.data.get(&index).unwrap_or(&self.default)
    }

    pub fn remove(&mut self, index: usize) {
        self.data.remove(&index);
    }

    pub fn len(&self) -> usize {
        self.data.len()
    }
}

impl<T: Default> Default for SparseArray<T> {
    fn default() -> Self {
        Self::new()
    }
}
