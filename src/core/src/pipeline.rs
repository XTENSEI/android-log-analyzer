pub trait Processor<T> {
    fn process(&self, item: T) -> Option<T>;
}

pub struct Pipeline<T> {
    processors: Vec<Box<dyn Processor<T>>>,
}

impl<T: Clone> Pipeline<T> {
    pub fn new() -> Self {
        Self {
            processors: Vec::new(),
        }
    }

    pub fn add<P: Processor<T> + 'static>(&mut self, processor: P) {
        self.processors.push(Box::new(processor));
    }

    pub fn execute(&self, item: T) -> Option<T> {
        let mut result = item;
        for processor in &self.processors {
            if let Some(processed) = processor.process(result.clone()) {
                result = processed;
            } else {
                return None;
            }
        }
        Some(result)
    }
}

impl<T> Default for Pipeline<T> {
    fn default() -> Self {
        Self::new()
    }
}
