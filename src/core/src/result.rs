use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Result<T, E> {
    value: Option<T>,
    error: Option<E>,
}

impl<T, E> Result<T, E> {
    pub fn ok(value: T) -> Self {
        Self {
            value: Some(value),
            error: None,
        }
    }

    pub fn err(error: E) -> Self {
        Self {
            value: None,
            error: Some(error),
        }
    }

    pub fn is_ok(&self) -> bool {
        self.value.is_some()
    }

    pub fn is_err(&self) -> bool {
        self.error.is_some()
    }

    pub fn unwrap(self) -> T {
        self.value.unwrap()
    }

    pub fn unwrap_err(self) -> E {
        self.error.unwrap()
    }
}
