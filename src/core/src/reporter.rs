pub struct Reporter;

impl Reporter {
    pub fn report_text(result: &crate::analyzer::AnalysisResult) -> String {
        let mut output = String::new();
        
        output.push_str("=== Log Analysis Results ===\n\n");
        output.push_str(&format!("Total Entries: {}\n", result.total_entries));
        output.push_str(&format!("Errors: {}\n", result.error_count));
        output.push_str(&format!("Warnings: {}\n", result.warning_count));
        output.push_str(&format!("Info: {}\n", result.info_count));
        output.push_str(&format!("Debug: {}\n", result.debug_count));
        output.push_str(&format!("\nScan Time: {}ms\n", result.scan_time_ms));
        output.push_str(&format!("\nIssues Found: {}\n", result.issues.len()));
        
        for issue in &result.issues {
            output.push_str(&format!(
                "[{:?}] {} - {} (line {}, count: {})\n",
                issue.severity, issue.category, issue.message, issue.line_number, issue.count
            ));
        }
        
        output
    }

    pub fn report_summary(result: &crate::analyzer::AnalysisResult) -> String {
        format!(
            "Analyzed {} entries: {} errors, {} warnings in {}ms",
            result.total_entries,
            result.error_count,
            result.warning_count,
            result.scan_time_ms
        )
    }
}
