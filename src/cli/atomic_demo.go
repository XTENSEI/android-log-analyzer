package main

import (
	"fmt"
	"sync/atomic"
)

func main() {
	var counter int64
	
	atomic.AddInt64(&counter, 1)
	atomic.AddInt64(&counter, 2)
	atomic.AddInt64(&counter, 3)
	
	fmt.Println("Counter:", atomic.LoadInt64(&counter))
}
