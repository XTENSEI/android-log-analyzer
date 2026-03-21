package main

import (
	"flag"
	"fmt"
	"os"
	"io"
)

func main() {
	flag.Parse()
	
	if flag.NArg() < 2 {
		fmt.Println("Usage: cp <src> <dst>")
		return
	}
	
	src := flag.Arg(0)
	dst := flag.Arg(1)
	
	from, err := os.Open(src)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer from.Close()
	
	to, err := os.Create(dst)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer to.Close()
	
	if _, err := io.Copy(to, from); err != nil {
		fmt.Println("Error:", err)
		return
	}
	
	fmt.Println("Copied:", src, "->", dst)
}
