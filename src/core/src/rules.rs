use crate::LogEntry;
use regex::Regex;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Rule {
    pub id: String,
    pub name: String,
    pub pattern: String,
    pub severity: IssueSeverity,
    pub category: String,
    pub description: String,
    pub enabled: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum IssueSeverity {
    Critical,
    High,
    Medium,
    Low,
    Info,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Issue {
    pub rule_id: String,
    pub severity: IssueSeverity,
    pub category: String,
    pub message: String,
    pub tag: String,
    pub line_number: usize,
    pub count: usize,
}

pub struct RuleEngine {
    rules: Vec<Rule>,
    compiled_patterns: HashMap<String, Regex>,
}

impl RuleEngine {
    pub fn new() -> Self {
        Self {
            rules: Vec::new(),
            compiled_patterns: HashMap::new(),
        }
    }

    pub fn add_rule(&mut self, rule: Rule) {
        if let Ok(re) = Regex::new(&rule.pattern) {
            self.compiled_patterns.insert(rule.id.clone(), re);
        }
        self.rules.push(rule);
    }

    pub fn add_default_rules(&mut self) {
        let default_rules = vec![
            Rule {
                id: "ANR".to_string(),
                name: "Application Not Responding".to_string(),
                pattern: r"ANR in|Reason:|CPU usage from".to_string(),
                severity: IssueSeverity::Critical,
                category: "Performance".to_string(),
                description: "Application not responding detected".to_string(),
                enabled: true,
            },
            Rule {
                id: "CRASH".to_string(),
                name: "Application Crash".to_string(),
                pattern: r"FATAL EXCEPTION|has died|Process.*died".to_string(),
                severity: IssueSeverity::Critical,
                category: "Stability".to_string(),
                description: "Application crash detected".to_string(),
                enabled: true,
            },
            Rule {
                id: "NPE".to_string(),
                name: "NullPointerException".to_string(),
                pattern: r"NullPointerException|Null pointer".to_string(),
                severity: IssueSeverity::High,
                category: "Code".to_string(),
                description: "Null pointer exception in code".to_string(),
                enabled: true,
            },
            Rule {
                id: "OOM".to_string(),
                name: "Out of Memory".to_string(),
                pattern: r"OutOfMemoryError|java.lang.OutOfMemoryError".to_string(),
                severity: IssueSeverity::Critical,
                category: "Memory".to_string(),
                description: "Out of memory error".to_string(),
                enabled: true,
            },
            Rule {
                id: "WTF".to_string(),
                name: "What a Terrible Failure".to_string(),
                pattern: r"WTF|What a terrible failure".to_string(),
                severity: IssueSeverity::High,
                category: "Stability".to_string(),
                description: "WTF error - unexpected condition".to_string(),
                enabled: true,
            },
            Rule {
                id: "LOW_MEMORY".to_string(),
                name: "Low Memory Warning".to_string(),
                pattern: r"low memory|killing|kswapd".to_string(),
                severity: IssueSeverity::Medium,
                category: "Memory".to_string(),
                description: "Low memory condition detected".to_string(),
                enabled: true,
            },
            Rule {
                id: "SECURITY".to_string(),
                name: "Security Issue".to_string(),
                pattern: r"SELinux|denied|permission".to_string(),
                severity: IssueSeverity::High,
                category: "Security".to_string(),
                description: "Security-related issue".to_string(),
                enabled: true,
            },
            Rule {
                id: "KILL".to_string(),
                name: "Process Killed".to_string(),
                pattern: r"killed|tombstone|signal".to_string(),
                severity: IssueSeverity::Critical,
                category: "Security".to_string(),
                description: "Process was killed".to_string(),
                enabled: true,
            },
            Rule {
                id: "BOOT".to_string(),
                name: "Boot Issue".to_string(),
                pattern: r"boot|cannot mount|failed to mount".to_string(),
                severity: IssueSeverity::High,
                category: "Boot".to_string(),
                description: "Boot issue".to_string(),
                enabled: true,
            },
            Rule {
                id: "FMARK".to_string(),
                name: "File Not Found".to_string(),
                pattern: r"FileNotFoundException|ENOENT".to_string(),
                severity: IssueSeverity::Medium,
                category: "File".to_string(),
                description: "File not found".to_string(),
                enabled: true,
            },
            Rule {
                id: "PERMISSION".to_string(),
                name: "Permission Denied".to_string(),
                pattern: r"SecurityException|permission denied".to_string(),
                severity: IssueSeverity::High,
                category: "Security".to_string(),
                description: "Permission denied".to_string(),
                enabled: true,
            },
            Rule {
                id: "SERVICE".to_string(),
                name: "Service Issue".to_string(),
                pattern: r"Service not found|cannot start service".to_string(),
                severity: IssueSeverity::High,
                category: "Service".to_string(),
                description: "Service issue".to_string(),
                enabled: true,
            },
            Rule {
                id: "BATTERY".to_string(),
                name: "Battery Issue".to_string(),
                pattern: r"battery|drain|voltage|temperature".to_string(),
                severity: IssueSeverity::Medium,
                category: "Power".to_string(),
                description: "Battery-related issue".to_string(),
                enabled: true,
            },
        ];

        for rule in default_rules {
            self.add_rule(rule);
        }
    }

    pub fn analyze(&self, entry: &LogEntry) -> Vec<Issue> {
        let mut issues = Vec::new();

        for rule in &self.rules {
            if !rule.enabled {
                continue;
            }

            if let Some(pattern) = self.compiled_patterns.get(&rule.id) {
                if pattern.is_match(&entry.message) || pattern.is_match(&entry.tag) {
                    issues.push(Issue {
                        rule_id: rule.id.clone(),
                        severity: rule.severity,
                        category: rule.category.clone(),
                        message: rule.description.clone(),
                        tag: entry.tag.clone(),
                        line_number: entry.line_number,
                        count: 1,
                    });
                }
            }
        }

        issues
    }
}

impl Default for RuleEngine {
    fn default() -> Self {
        Self::new()
    }
}
