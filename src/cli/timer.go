package main

import (
	"fmt"
	"time"
)

func main() {
	timer := time.NewTimer(2 * time.Second)
	defer timer.Stop()
	
	<-timer.C
	fmt.Println("Timer fired!")
}
