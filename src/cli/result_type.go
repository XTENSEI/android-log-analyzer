package main

import (
	"fmt"
)

type Result struct {
	Ok  bool
	Val interface{}
}

func Success(val interface{}) Result {
	return Result{true, val}
}

func Fail(val interface{}) Result {
	return Result{false, val}
}

func main() {
	r := Success(42)
	fmt.Println("OK:", r.Ok, "Value:", r.Val)
}
