use std::sync::{Arc, Mutex};

pub struct State<T> {
    value: Arc<Mutex<T>>,
}

impl<T> State<T> {
    pub fn new(value: T) -> Self {
        Self {
            value: Arc::new(Mutex::new(value)),
        }
    }

    pub fn get(&self) -> T where T: Clone {
        self.value.lock().unwrap().clone()
    }

    pub fn set(&self, value: T) {
        *self.value.lock().unwrap() = value;
    }

    pub fn update<F>(&self, f: F) where F: FnOnce(&mut T) {
        let mut v = self.value.lock().unwrap();
        f(&mut v);
    }
}
