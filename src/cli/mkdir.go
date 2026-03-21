package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: mkdirdemo <path>")
		return
	}
	
	path := os.Args[1]
	
	if err := os.MkdirAll(path, 0755); err != nil {
		fmt.Println("Error:", err)
		return
	}
	
	abs, _ := filepath.Abs(path)
	fmt.Println("Created:", abs)
}
