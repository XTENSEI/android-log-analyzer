package main

import (
	"flag"
	"fmt"
)

type Config struct {
	Host string
	Port int
}

func main() {
	host := flag.String("host", "localhost", "Server host")
	port := flag.Int("port", 8080, "Server port")
	flag.Parse()
	
	cfg := Config{
		Host: *host,
		Port: *port,
	}
	
	fmt.Printf("Config: %+v\n", cfg)
}
