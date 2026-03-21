package main

import (
	"fmt"
	"strings"
)

func main() {
	s := "Hello, World!"
	fmt.Println("Upper:", strings.ToUpper(s))
	fmt.Println("Lower:", strings.ToLower(s))
	fmt.Println("Contains World:", strings.Contains(s, "World"))
	fmt.Println("HasPrefix Hello:", strings.HasPrefix(s, "Hello"))
}
