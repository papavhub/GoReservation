package handlers

type HelloResponse struct {
	Message string `json:"message"`
	Count   int    `json:"count"`
}

type ErrorResponse struct {
	Message string `json:"message"`
}
