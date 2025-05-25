package main

import (
	"encoding/json"
	"net/http"
	"sync"
	"time"
)

type Request struct {
	URLs []string `json:"urls"`
}

type Response struct {
	URL        string `json:"url"`
	StatusCode int    `json:"http_status_code"`
}

func fetchURL(url string, wg *sync.WaitGroup, results chan<- Response) {
	defer wg.Done()
	client := http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		results <- Response{URL: url, StatusCode: 0}
		return
	}
	results <- Response{URL: url, StatusCode: resp.StatusCode}
}

func fetchHandler(w http.ResponseWriter, r *http.Request) {
	var req Request
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		return
	}

	var wg sync.WaitGroup
	results := make(chan Response, len(req.URLs))

	for _, url := range req.URLs {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	response := make([]Response, 0)
	for result := range results {
		response = append(response, result)
	}

	err = json.NewEncoder(w).Encode(response)
	if err != nil {
		return
	}
}

func main() {
	http.HandleFunc("/fetch", fetchHandler)
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		return
	}
}
