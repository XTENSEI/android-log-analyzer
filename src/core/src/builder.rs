pub struct Builder<T> {
    value: Option<T>,
}

impl<T> Builder<T> {
    pub fn new() -> Self {
        Self { value: None }
    }

    pub fn with(mut self, value: T) -> Self {
        self.value = Some(value);
        self
    }

    pub fn build(self) -> Option<T> {
        self.value
    }
}

impl<T> Default for Builder<T> {
    fn default() -> Self {
        Self::new()
    }
}
