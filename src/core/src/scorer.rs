use std::collections::HashMap;

pub struct WeightedScore {
    weights: HashMap<String, f64>,
}

impl WeightedScore {
    pub fn new() -> Self {
        let mut weights = HashMap::new();
        weights.insert("Critical".to_string(), 10.0);
        weights.insert("High".to_string(), 5.0);
        weights.insert("Medium".to_string(), 2.0);
        weights.insert("Low".to_string(), 1.0);
        
        Self { weights }
    }

    pub fn score(&self, severity: &str) -> f64 {
        *self.weights.get(severity).unwrap_or(&0.0)
    }

    pub fn total_score(&self, issues: &[(&str, usize)]) -> f64 {
        issues.iter().map(|(sev, count)| self.score(sev) * *count as f64).sum()
    }
}

impl Default for WeightedScore {
    fn default() -> Self {
        Self::new()
    }
}
