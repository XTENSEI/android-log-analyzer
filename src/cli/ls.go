package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	flag.Parse()
	
	dir := "."
	if flag.NArg() > 0 {
		dir = flag.Arg(0)
	}
	
	entries, err := os.ReadDir(dir)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	
	for _, entry := range entries {
		info, _ := entry.Info()
		size := info.Size()
		name := entry.Name()
		
		if entry.IsDir() {
			fmt.Printf("d %s/\n", name)
		} else {
			fmt.Printf("- %s (%d bytes)\n", name, size)
		}
	}
}
