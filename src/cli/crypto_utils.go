package main

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
)

func main() {
	data := make([]byte, 32)
	rand.Read(data)
	encoded := base64.StdEncoding.EncodeToString(data)
	fmt.Println("Random:", encoded)
}
