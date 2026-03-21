package main

import (
	"fmt"
	"time"
)

type Progress struct {
	Total   int
	Current int
	Start   time.Time
}

func (p *Progress) Update(current int) {
	p.Current = current
}

func (p *Progress) Percent() float64 {
	if p.Total == 0 {
		return 0
	}
	return float64(p.Current) / float64(p.Total) * 100
}

func (p *Progress) Elapsed() time.Duration {
	return time.Since(p.Start)
}

func (p *Progress) Estimate() time.Duration {
	if p.Current == 0 {
		return 0
	}
	
	elapsed := time.Since(p.Start)
	perItem := elapsed / time.Duration(p.Current)
	remaining := p.Total - p.Current
	return perItem * time.Duration(remaining)
}

func main() {
	p := Progress{
		Total: 100,
		Start: time.Now(),
	}
	
	for i := 0; i <= 100; i += 10 {
		p.Update(i)
		fmt.Printf("Progress: %.1f%% (ETA: %v)\n", p.Percent(), p.Estimate())
		time.Sleep(100 * time.Millisecond)
	}
}
