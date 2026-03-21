package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: %s [options] <logdir>\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "\nOptions:\n")
		flag.PrintDefaults()
	}
	
	flag.Parse()
	
	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}
	
	dir := flag.Arg(0)
	
	logs, err := filepath.Glob(filepath.Join(dir, "*.log"))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	
	fmt.Printf("Found %d log files:\n", len(logs))
	for _, log := range logs {
		info, err := os.Stat(log)
		if err != nil {
			continue
		}
		fmt.Printf("  - %s (%.1f MB)\n", filepath.Base(log), float64(info.Size())/1024/1024)
	}
}
