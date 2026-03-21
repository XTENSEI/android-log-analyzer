package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

type AnalysisResult struct {
	TotalEntries      int            `json:"total_entries"`
	ErrorCount        int            `json:"error_count"`
	WarningCount      int            `json:"warning_count"`
	InfoCount         int            `json:"info_count"`
	DebugCount        int            `json:"debug_count"`
	Tags              map[string]int `json:"tags"`
	Issues            []Issue        `json:"issues"`
	IssuesBySeverity  map[string]int `json:"issues_by_severity"`
	IssuesByCategory  map[string]int `json:"issues_by_category"`
	TopTags           [][2]int       `json:"top_tags"`
	ScanTimeMs        int            `json:"scan_time_ms"`
}

type Issue struct {
	RuleID    string `json:"rule_id"`
	Severity  string `json:"severity"`
	Category  string `json:"category"`
	Message   string `json:"message"`
	Tag       string `json:"tag"`
	LineNumber int   `json:"line_number"`
	Count     int    `json:"count"`
}

var (
	binaryPath string
	outputJSON bool
	verbose    bool
)

func init() {
	flag.StringVar(&binaryPath, "bin", findBinary(), "Path to loganalyzer binary")
	flag.BoolVar(&outputJSON, "json", false, "Output in JSON format")
	flag.BoolVar(&verbose, "v", false, "Verbose output")
}

func findBinary() string {
	paths := []string{
		"../core/target/release/loganalyzer",
		"../../core/target/release/loganalyzer",
		"./loganalyzer",
		"/usr/local/bin/loganalyzer",
	}
	
	for _, p := range paths {
		if _, err := os.Stat(p); err == nil {
			return p
		}
	}
	
	return paths[0]
}

func main() {
	flag.Parse()
	
	if flag.NArg() < 1 {
		fmt.Fprintf(os.Stderr, "Usage: %s <logfile> [options]\n", os.Args[0])
		flag.PrintDefaults()
		os.Exit(1)
	}
	
	logFile := flag.Arg(0)
	
	if _, err := os.Stat(logFile); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "Error: file not found: %s\n", logFile)
		os.Exit(1)
	}
	
	args := []string{}
	if outputJSON {
		args = append(args, "--output", "json")
	}
	args = append(args, logFile)
	
	cmd := exec.Command(binaryPath, args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	
	if err := cmd.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error running analyzer: %v\n", err)
		os.Exit(1)
	}
}

func printSummary(result *AnalysisResult) {
	fmt.Println("=== Log Analysis Results ===\n")
	fmt.Printf("Total Entries: %d\n", result.TotalEntries)
	fmt.Printf("Errors: %d\n", result.ErrorCount)
	fmt.Printf("Warnings: %d\n", result.WarningCount)
	fmt.Printf("Info: %d\n", result.InfoCount)
	fmt.Printf("Debug: %d\n", result.DebugCount)
	fmt.Printf("\nScan Time: %dms\n", result.ScanTimeMs)
	fmt.Printf("\nIssues Found: %d\n", len(result.Issues))
}

func printIssues(result *AnalysisResult) {
	for _, issue := range result.Issues {
		fmt.Printf("[%s] %s - %s (line %d, count: %d)\n",
			issue.Severity, issue.Category, issue.Message, issue.LineNumber, issue.Count)
	}
}

func runAnalyzerJSON(logFile string) (*AnalysisResult, error) {
	args := []string{"--output", "json", logFile}
	
	cmd := exec.Command(binaryPath, args...)
	output, err := cmd.Output()
	if err != nil {
		return nil, err
	}
	
	var result AnalysisResult
	if err := json.Unmarshal(output, &result); err != nil {
		return nil, err
	}
	
	return &result, nil
}

func ensureBinaryExists() error {
	if _, err := os.Stat(binaryPath); os.IsNotExist(err) {
		return fmt.Errorf("binary not found at: %s", binaryPath)
	}
	return nil
}

func getBinaryDir() string {
	execPath, _ := os.Executable()
	return filepath.Dir(execPath)
}
