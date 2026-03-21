package main

import (
	"fmt"
	"os"
)

func main() {
	env := os.Environ()
	fmt.Println("Environment variables:")
	for _, e := range env {
		fmt.Println(e)
	}
}
