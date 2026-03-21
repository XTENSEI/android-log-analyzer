package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	flag.Parse()
	
	if flag.NArg() < 1 {
		fmt.Println("Usage: rm <path>")
		return
	}
	
	path := flag.Arg(0)
	
	if err := os.RemoveAll(path); err != nil {
		fmt.Println("Error:", err)
		return
	}
	
	fmt.Println("Removed:", path)
}
