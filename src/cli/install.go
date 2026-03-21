package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: install <destination>")
		os.Exit(1)
	}
	
	dest := os.Args[1]
	
	binary := "loganalyzer"
	if _, err := os.Stat(binary); err != nil {
		fmt.Println("Error: binary not found")
		os.Exit(1)
	}
	
	destPath := filepath.Join(dest, binary)
	
	if err := os.CopyFile(binary, destPath); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
	
	if err := os.Chmod(destPath, 0755); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
	
	fmt.Println("Installed to:", destPath)
}

func CopyFile(src, dst string) error {
	from, err := os.Open(src)
	if err != nil {
		return err
	}
	defer from.Close()
	
	to, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer to.Close()
	
	_, err = from.WriteTo(to)
	return err
}
