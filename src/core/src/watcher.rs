use std::path::PathBuf;

pub struct Watcher {
    paths: Vec<PathBuf>,
}

impl Watcher {
    pub fn new() -> Self {
        Self {
            paths: Vec::new(),
        }
    }

    pub fn watch(&mut self, path: PathBuf) {
        self.paths.push(path);
    }

    pub fn paths(&self) -> &[PathBuf] {
        &self.paths
    }

    pub fn unwatch(&mut self, path: &PathBuf) {
        self.paths.retain(|p| p != path);
    }
}

impl Default for Watcher {
    fn default() -> Self {
        Self::new()
    }
}
