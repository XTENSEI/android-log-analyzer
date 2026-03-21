package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: %s <command>\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "\nCommands:\n")
		fmt.Fprintf(os.Stderr, "  build    Build the analyzer\n")
		fmt.Fprintf(os.Stderr, "  run      Run the analyzer\n")
		fmt.Fprintf(os.Stderr, "  test     Run tests\n")
	}
	flag.Parse()
	
	if flag.NArg() < 1 {
		flag.Usage()
		os.Exit(1)
	}
	
	cmd := flag.Arg(0)
	
	switch cmd {
	case "build":
		fmt.Println("Building...")
	case "run":
		fmt.Println("Running...")
	case "test":
		fmt.Println("Testing...")
	default:
		fmt.Printf("Unknown command: %s\n", cmd)
		flag.Usage()
		os.Exit(1)
	}
}
