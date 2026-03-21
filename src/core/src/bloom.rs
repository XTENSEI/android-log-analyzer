use std::collections::HashSet;

pub struct BloomFilter {
    bits: Vec<bool>,
    size: usize,
    hashes: usize,
}

impl BloomFilter {
    pub fn new(size: usize, hashes: usize) -> Self {
        Self {
            bits: vec![false; size],
            size,
            hashes,
        }
    }

    fn hash(&self, item: &str, seed: usize) -> usize {
        let mut hash = 0;
        for (i, byte) in item.bytes().enumerate() {
            hash = hash.wrapping_mul(31).wrapping_add((byte as usize).wrapping_mul(seed + i));
        }
        hash % self.size
    }

    pub fn add(&mut self, item: &str) {
        for i in 0..self.hashes {
            let idx = self.hash(item, i);
            self.bits[idx] = true;
        }
    }

    pub fn contains(&self, item: &str) -> bool {
        for i in 0..self.hashes {
            let idx = self.hash(item, i);
            if !self.bits[idx] {
                return false;
            }
        }
        true
    }
}
