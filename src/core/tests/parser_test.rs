use loganalyzer::parser::LogParser;
use loganalyzer::LogLevel;

#[test]
fn test_parse_valid_line() {
    let line = "01-15 10:23:45.123  1000  2000 I ActivityManager: Starting activity";
    let entry = LogParser::parse_line(line).unwrap();
    
    assert_eq!(entry.level, LogLevel::Info);
    assert_eq!(entry.tag, "ActivityManager");
    assert_eq!(entry.pid, 1000);
    assert_eq!(entry.tid, 2000);
}

#[test]
fn test_parse_empty_line() {
    let line = "";
    let entry = LogParser::parse_line(line);
    assert!(entry.is_none());
}

#[test]
fn test_parse_invalid_line() {
    let line = "not a valid log line";
    let entry = LogParser::parse_line(line);
    assert!(entry.is_none());
}

#[test]
fn test_log_level_from_char() {
    assert_eq!(LogLevel::Verbose, LogLevel::from('V'));
    assert_eq!(LogLevel::Debug, LogLevel::from('D'));
    assert_eq!(LogLevel::Info, LogLevel::from('I'));
    assert_eq!(LogLevel::Warning, LogLevel::from('W'));
    assert_eq!(LogLevel::Error, LogLevel::from('E'));
    assert_eq!(LogLevel::Fatal, LogLevel::from('F'));
    assert_eq!(LogLevel::Unknown, LogLevel::from('X'));
}
