package main

import (
	"fmt"
	"context"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	
	select {
	case <-time.After(1 * time.Second):
		fmt.Println("Done")
	case <-ctx.Done():
		fmt.Println("Cancelled:", ctx.Err())
	}
}
