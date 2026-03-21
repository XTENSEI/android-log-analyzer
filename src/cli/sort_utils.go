package main

import (
	"fmt"
	"sort"
)

func main() {
	ints := []int{5, 2, 8, 1, 9}
	sort.Ints(ints)
	fmt.Println("Sorted:", ints)
	
	strs := []string{"banana", "apple", "cherry"}
	sort.Strings(strs)
	fmt.Println("Sorted:", strs)
}
