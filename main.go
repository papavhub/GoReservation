package main

import (
	"net/http"

	"github.com/gin-gonic/gin"

	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"

	_ "gin-hello/docs"
)

// @title Gin Hello API
// @version 1.0
// @description Gin Swagger Example
// @host localhost:8080
// @BasePath /
func main() {
	r := gin.Default()

	r.GET("/hello", Hello)

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	r.Run(":8080")
}

// Hello godoc
// @Summary Hello World
// @Description 간단한 헬로월드 API
// @Tags hello
// @Produce json
// @Success 200 {object} map[string]string
// @Router /hello [get]
func Hello(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"message": "Hello, Gin!",
	})
}
