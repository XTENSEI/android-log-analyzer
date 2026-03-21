package main

import (
	"fmt"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			fmt.Println("Goroutine", n)
		}(i)
	}
	
	wg.Wait()
	fmt.Println("Done")
}
