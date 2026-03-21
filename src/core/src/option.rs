pub struct Option<T> {
    value: Option<T>,
}

impl<T> Option<T> {
    pub fn some(value: T) -> Self {
        Self { value: Some(value) }
    }

    pub fn none() -> Self {
        Self { value: None }
    }

    pub fn is_some(&self) -> bool {
        self.value.is_some()
    }

    pub fn is_none(&self) -> bool {
        self.value.is_none()
    }

    pub fn unwrap(self) -> T {
        self.value.unwrap()
    }

    pub fn unwrap_or(self, default: T) -> T {
        self.value.unwrap_or(default)
    }

    pub fn map<U, F>(self, f: F) -> Option<U>
    where
        F: FnOnce(T) -> U,
    {
        match self.value {
            Some(v) => Option::some(f(v)),
            None => Option::none(),
        }
    }
}
