package main

import (
	"fmt"
)

type Queue struct {
	items []interface{}
}

func (q *Queue) Enqueue(item interface{}) {
	q.items = append(q.items, item)
}

func (q *Queue) Dequeue() interface{} {
	if len(q.items) == 0 {
		return nil
	}
	item := q.items[0]
	q.items = q.items[1:]
	return item
}

func (q *Queue) Peek() interface{} {
	if len(q.items) == 0 {
		return nil
	}
	return q.items[0]
}

func main() {
	q := Queue{}
	q.Enqueue(1)
	q.Enqueue(2)
	fmt.Println("Dequeue:", q.Dequeue())
	fmt.Println("Peek:", q.Peek())
}
