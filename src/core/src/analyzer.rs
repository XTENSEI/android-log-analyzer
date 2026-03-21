use crate::rules::{Issue, IssueSeverity, RuleEngine};
use crate::LogLevel;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnalysisResult {
    pub total_entries: usize,
    pub error_count: usize,
    pub warning_count: usize,
    pub info_count: usize,
    pub debug_count: usize,
    pub tags: HashMap<String, usize>,
    pub issues: Vec<Issue>,
    pub issues_by_severity: HashMap<String, usize>,
    pub issues_by_category: HashMap<String, usize>,
    pub top_tags: Vec<(String, usize)>,
    pub scan_time_ms: u64,
}

impl AnalysisResult {
    pub fn new() -> Self {
        Self {
            total_entries: 0,
            error_count: 0,
            warning_count: 0,
            info_count: 0,
            debug_count: 0,
            tags: HashMap::new(),
            issues: Vec::new(),
            issues_by_severity: HashMap::new(),
            issues_by_category: HashMap::new(),
            top_tags: Vec::new(),
            scan_time_ms: 0,
        }
    }
}

pub struct Analyzer {
    rule_engine: RuleEngine,
}

impl Analyzer {
    pub fn new() -> Self {
        let mut rule_engine = RuleEngine::new();
        rule_engine.add_default_rules();
        Self { rule_engine }
    }

    pub fn analyze_file<P: AsRef<Path>>(&self, path: P) -> Result<AnalysisResult, String> {
        let start = std::time::Instant::now();
        let file = File::open(path).map_err(|e| e.to_string())?;
        let reader = BufReader::with_capacity(65536, file);

        let mut result = AnalysisResult::new();
        let mut issue_map: HashMap<String, Issue> = HashMap::new();

        for line_result in reader.lines() {
            if let Ok(line) = line_result {
                result.total_entries += 1;

                if let Some(entry) = crate::parser::LogParser::parse_line(&line) {
                    match entry.level {
                        LogLevel::Error | LogLevel::Fatal => result.error_count += 1,
                        LogLevel::Warning => result.warning_count += 1,
                        LogLevel::Info => result.info_count += 1,
                        LogLevel::Debug => result.debug_count += 1,
                        _ => {}
                    }

                    *result.tags.entry(entry.tag.clone()).or_insert(0) += 1;

                    let issues = self.rule_engine.analyze(&entry);
                    for issue in issues {
                        let key = format!("{}:{}:{}", issue.rule_id, issue.tag, issue.line_number);
                        if let Some(existing) = issue_map.get_mut(&key) {
                            existing.count += 1;
                        } else {
                            issue_map.insert(key, issue);
                        }
                    }
                }
            }
        }

        for (_, issue) in issue_map.drain() {
            let sev_key = format!("{:?}", issue.severity);
            *result.issues_by_severity.entry(sev_key).or_insert(0) += issue.count;
            *result.issues_by_category.entry(issue.category.clone()).or_insert(0) += issue.count;
            result.issues.push(issue);
        }

        result.issues.sort_by(|a, b| {
            let sev_order = |s: &IssueSeverity| match s {
                IssueSeverity::Critical => 0,
                IssueSeverity::High => 1,
                IssueSeverity::Medium => 2,
                IssueSeverity::Low => 3,
                IssueSeverity::Info => 4,
            };
            sev_order(&a.severity).cmp(&sev_order(&b.severity))
        });

        let mut tags: Vec<_> = result.tags.drain().collect();
        tags.sort_by(|a, b| b.1.cmp(&a.1));
        result.top_tags = tags.into_iter().take(20).collect();

        result.scan_time_ms = start.elapsed().as_millis() as u64;

        Ok(result)
    }

    pub fn with_custom_rules(mut self, rules: Vec<crate::rules::Rule>) -> Self {
        for rule in rules {
            self.rule_engine.add_rule(rule);
        }
        self
    }
}

impl Default for Analyzer {
    fn default() -> Self {
        Self::new()
    }
}
