package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()
	fmt.Println("Now:", now.Format("2006-01-02 15:04:05"))
	
	tomorrow := now.Add(24 * time.Hour)
	fmt.Println("Tomorrow:", tomorrow.Format("2006-01-02"))
	
	diff := tomorrow.Sub(now)
	fmt.Println("Diff:", diff.Hours(), "hours")
}
