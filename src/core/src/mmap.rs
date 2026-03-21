use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

use crate::parser::LogParser;

pub struct StreamingParser {
    chunk_size: usize,
}

impl StreamingParser {
    pub fn new() -> Self {
        Self {
            chunk_size: 65536,
        }
    }

    pub fn with_chunk_size(mut self, size: usize) -> Self {
        self.chunk_size = size;
        self
    }

    pub fn process_file<F>(&self, path: &Path, mut callback: F) -> Result<usize, String>
    where
        F: FnMut(String) -> bool,
    {
        let file = File::open(path).map_err(|e| e.to_string())?;
        let reader = BufReader::with_capacity(self.chunk_size, file);
        
        let mut count = 0;
        
        for line in reader.lines() {
            match line {
                Ok(line) => {
                    if !callback(line) {
                        break;
                    }
                    count += 1;
                }
                Err(_) => continue,
            }
        }
        
        Ok(count)
    }

    pub fn count_lines(&self, path: &Path) -> Result<usize, String> {
        let file = File::open(path).map_err(|e| e.to_string())?;
        let reader = BufReader::with_capacity(self.chunk_size, file);
        
        Ok(reader.lines().count())
    }
}

impl Default for StreamingParser {
    fn default() -> Self {
        Self::new()
    }
}
