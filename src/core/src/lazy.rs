pub struct Lazy<T> {
    value: Option<T>,
    init: fn() -> T,
}

impl<T> Lazy<T> {
    pub fn new(init: fn() -> T) -> Self {
        Self {
            value: None,
            init,
        }
    }

    pub fn get(&mut self) -> &T {
        if self.value.is_none() {
            self.value = Some((self.init)());
        }
        self.value.as_ref().unwrap()
    }
}
