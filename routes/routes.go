package routes

import (
	"github.com/gin-gonic/gin"
	"gin-hello/handlers"
)

func RegisterRoutes(r *gin.Engine) {
	r.GET("/hello", handlers.Hello)
	r.GET("/health", handlers.Health)
}
