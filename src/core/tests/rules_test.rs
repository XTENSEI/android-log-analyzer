use loganalyzer::rules::{Rule, RuleEngine, IssueSeverity};

#[test]
fn test_rule_engine_add_rule() {
    let mut engine = RuleEngine::new();
    
    let rule = Rule {
        id: "TEST".to_string(),
        name: "Test Rule".to_string(),
        pattern: "test".to_string(),
        severity: IssueSeverity::Medium,
        category: "Test".to_string(),
        description: "Test rule".to_string(),
        enabled: true,
    };
    
    engine.add_rule(rule);
    
    assert_eq!(engine.analyze(&loganalyzer::LogEntry {
        timestamp: 0,
        level: loganalyzer::LogLevel::Info,
        tag: "test".to_string(),
        pid: 0,
        tid: 0,
        message: "test message".to_string(),
        line_number: 0,
    }).len(), 1);
}

#[test]
fn test_rule_engine_default_rules() {
    let engine = RuleEngine::new();
    
    let mut engine_with_defaults = RuleEngine::new();
    engine_with_defaults.add_default_rules();
}
