use clap::{Parser, ValueEnum};
use loganalyzer::analyzer::Analyzer;
use loganalyzer::rules::IssueSeverity;
use serde_json::to_string_pretty;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(name = "loganalyzer")]
#[command(about = "High-performance Android log analyzer", long_about = None)]
struct Args {
    #[arg(short, long, value_name = "FILE")]
    input: PathBuf,

    #[arg(short, long, value_name = "FORMAT", default_value = "json")]
    output: OutputFormat,

    #[arg(short, long)]
    verbose: bool,

    #[arg(long, value_enum)]
    severity: Option<FilterSeverity>,
}

#[derive(Debug, Clone, ValueEnum)]
enum OutputFormat {
    Json,
    Text,
    Summary,
}

#[derive(Debug, Clone, ValueEnum)]
enum FilterSeverity {
    Critical,
    High,
    Medium,
    Low,
    Info,
}

fn main() {
    env_logger::init();
    let args = Args::parse();

    let analyzer = Analyzer::new();

    match analyzer.analyze_file(&args.input) {
        Ok(result) => match args.output {
            OutputFormat::Json => {
                let json = to_string_pretty(&result).unwrap();
                println!("{}", json);
            }
            OutputFormat::Text => {
                println!("=== Log Analysis Results ===\n");
                println!("Total Entries: {}", result.total_entries);
                println!("Errors: {}", result.error_count);
                println!("Warnings: {}", result.warning_count);
                println!("Info: {}", result.info_count);
                println!("Debug: {}", result.debug_count);
                println!("\nScan Time: {}ms", result.scan_time_ms);
            }
            OutputFormat::Summary => {
                println!("=== Issues Found: {} ===\n", result.issues.len());
                for issue in &result.issues {
                    if let Some(ref filter) = args.severity {
                        let filter_val = match filter {
                            FilterSeverity::Critical => IssueSeverity::Critical,
                            FilterSeverity::High => IssueSeverity::High,
                            FilterSeverity::Medium => IssueSeverity::Medium,
                            FilterSeverity::Low => IssueSeverity::Low,
                            FilterSeverity::Info => IssueSeverity::Info,
                        };
                        if issue.severity != filter_val {
                            continue;
                        }
                    }
                    println!(
                        "[{:?}] {} - {} (line {}, count: {})",
                        issue.severity, issue.category, issue.message, issue.line_number, issue.count
                    );
                }
            }
        },
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}
