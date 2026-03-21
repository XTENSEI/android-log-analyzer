package main

import (
	"fmt"
	"sync"
)

type Pool struct {
	workers int
	jobs   chan func()
	wg     sync.WaitGroup
}

func NewPool(workers int) *Pool {
	return &Pool{
		workers: workers,
		jobs:    make(chan func(), 100),
	}
}

func (p *Pool) Start() {
	for i := 0; i < p.workers; i++ {
		p.wg.Add(1)
		go func() {
			defer p.wg.Done()
			for job := range p.jobs {
				job()
			}
		}()
	}
}

func (p *Pool) Submit(job func()) {
	p.jobs <- job
}

func (p *Pool) Stop() {
	close(p.jobs)
	p.wg.Wait()
}

func main() {
	pool := NewPool(4)
	pool.Start()
	
	pool.Submit(func() { fmt.Println("Job 1") })
	pool.Submit(func() { fmt.Println("Job 2") })
	
	pool.Stop()
}
