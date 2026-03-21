package main

import (
	"fmt"
)

func main() {
	cache := make(map[string]string)
	
	cache["key1"] = "value1"
	cache["key2"] = "value2"
	
	if val, ok := cache["key1"]; ok {
		fmt.Println("key1:", val)
	}
	
	delete(cache, "key2")
	
	fmt.Println("Cache:", cache)
}
