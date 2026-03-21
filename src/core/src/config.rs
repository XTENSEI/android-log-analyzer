use crate::rules::{Rule, RuleEngine};
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;
use std::path::Path;

pub struct AnalyzerConfig {
    pub binary_path: Option<PathBuf>,
    pub rules_dir: Option<PathBuf>,
    pub max_file_size: u64,
    pub timeout_seconds: u64,
    pub streaming_mode: bool,
}

impl AnalyzerConfig {
    pub fn new() -> Self {
        Self {
            binary_path: None,
            rules_dir: None,
            max_file_size: 500 * 1024 * 1024,
            timeout_seconds: 300,
            streaming_mode: true,
        }
    }

    pub fn with_binary_path(mut self, path: PathBuf) -> Self {
        self.binary_path = Some(path);
        self
    }

    pub fn with_rules_dir(mut self, path: PathBuf) -> Self {
        self.rules_dir = Some(path);
        self
    }

    pub fn with_max_file_size(mut self, size: u64) -> Self {
        self.max_file_size = size;
        self
    }

    pub fn with_timeout(mut self, seconds: u64) -> Self {
        self.timeout_seconds = seconds;
        self
    }
}

impl Default for AnalyzerConfig {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Debug, Deserialize)]
struct RuleFile {
    rules: Vec<RuleDefinition>,
}

#[derive(Debug, Deserialize)]
struct RuleDefinition {
    #[serde(rename = "id")]
    id: String,
    #[serde(rename = "name")]
    name: String,
    #[serde(rename = "pattern")]
    pattern: String,
    #[serde(rename = "severity")]
    severity: String,
    #[serde(rename = "category")]
    category: String,
    #[serde(rename = "description")]
    description: String,
    #[serde(rename = "enabled", default = "default_enabled")]
    enabled: bool,
}

fn default_enabled() -> bool {
    true
}

impl RuleEngine {
    pub fn load_rules_from_file<P: AsRef<Path>>(&mut self, path: P) -> Result<usize, String> {
        let content = fs::read_to_string(path).map_err(|e| e.to_string())?;
        let rule_file: RuleFile = serde_json::from_str(&content).map_err(|e| e.to_string())?;
        
        let count = rule_file.rules.len();
        
        for def in rule_file.rules {
            let severity = match def.severity.to_lowercase().as_str() {
                "critical" => crate::rules::IssueSeverity::Critical,
                "high" => crate::rules::IssueSeverity::High,
                "medium" => crate::rules::IssueSeverity::Medium,
                "low" => crate::rules::IssueSeverity::Low,
                _ => crate::rules::IssueSeverity::Info,
            };
            
            let rule = Rule {
                id: def.id,
                name: def.name,
                pattern: def.pattern,
                severity,
                category: def.category,
                description: def.description,
                enabled: def.enabled,
            };
            
            self.add_rule(rule);
        }
        
        Ok(count)
    }
    
    pub fn load_rules_from_directory<P: AsRef<Path>>(&mut self, dir: P) -> Result<usize, String> {
        let mut total = 0;
        let path = dir.as_ref();
        
        if !path.is_dir() {
            return Err("Not a directory".to_string());
        }
        
        for entry in fs::read_dir(path).map_err(|e| e.to_string())? {
            let entry = entry.map_err(|e| e.to_string())?;
            let path = entry.path();
            
            if path.extension().map_or(false, |ext| ext == "json") {
                match self.load_rules_from_file(&path) {
                    Ok(count) => {
                        println!("Loaded {} rules from {:?}", count, path.file_name());
                        total += count;
                    }
                    Err(e) => {
                        eprintln!("Failed to load rules from {:?}: {}", path.file_name(), e);
                    }
                }
            }
        }
        
        Ok(total)
    }
}
