package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Config struct {
	BinaryPath string `json:"binary_path"`
	MaxFileSize int64 `json:"max_file_size"`
	Timeout int `json:"timeout"`
}

func LoadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}
	
	return &cfg, nil
}

func SaveConfig(cfg *Config, path string) error {
	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return err
	}
	
	return os.WriteFile(path, data, 0644)
}

func main() {
	cfg := &Config{
		BinaryPath: "./loganalyzer",
		MaxFileSize: 500 * 1024 * 1024,
		Timeout: 300,
	}
	
	if err := SaveConfig(cfg, "config.json"); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
	
	fmt.Println("Config saved")
}
