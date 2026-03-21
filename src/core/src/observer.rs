pub struct Observer<T> {
    callbacks: Vec<Box<dyn Fn(&T) + Send + Sync>>,
}

impl<T> Observer<T> {
    pub fn new() -> Self {
        Self {
            callbacks: Vec::new(),
        }
    }

    pub fn subscribe<F>(&mut self, callback: F)
    where
        F: Fn(&T) + Send + Sync + 'static,
    {
        self.callbacks.push(Box::new(callback));
    }

    pub fn notify(&self, data: &T) {
        for callback in &self.callbacks {
            callback(data);
        }
    }
}

impl<T> Default for Observer<T> {
    fn default() -> Self {
        Self::new()
    }
}
