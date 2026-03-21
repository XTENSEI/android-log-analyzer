package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	
	fmt.Print("Enter name: ")
	name, _ := reader.ReadString('\n')
	
	fmt.Print("Enter value: ")
	value, _ := reader.ReadString('\n')
	
	fmt.Println("Name:", name)
	fmt.Println("Value:", value)
}
