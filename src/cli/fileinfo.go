package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	flag.Parse()
	
	path := "."
	if flag.NArg() > 0 {
		path = flag.Arg(0)
	}
	
	info, err := os.Stat(path)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	
	fmt.Println("Path:", path)
	fmt.Println("Size:", info.Size())
	fmt.Println("Mode:", info.Mode())
	fmt.Println("ModTime:", info.ModTime())
}
