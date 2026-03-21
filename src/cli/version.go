package main

import (
	"flag"
	"fmt"
)

type VersionFlag struct {
	value string
}

func (v *VersionFlag) Set(s string) error {
	v.value = s
	return nil
}

func (v *VersionFlag) String() string {
	return v.value
}

func main() {
	v := &VersionFlag{}
	flag.Var(v, "version", "version string")
	
	flag.Parse()
	
	fmt.Println("Version:", v.value)
}
