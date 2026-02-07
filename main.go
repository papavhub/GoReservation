package main

import (
	"github.com/gin-gonic/gin"

	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"

	"gin-hello/routes"
	_ "gin-hello/docs"
)

// @title Gin Hello API
// @version 1.0
// @description Gin Swagger Example
// @host localhost:8080
// @BasePath /
func main() {
	r := gin.Default()

	routes.RegisterRoutes(r)

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	r.Run(":8080")
}
