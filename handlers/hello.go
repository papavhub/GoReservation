package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

// Hello godoc
// @Summary Hello World
// @Description name과 count를 받아서 인사 메시지 반환
// @Tags hello
// @Produce json
// @Param name query string true "이름"
// @Param count query int false "반복 횟수" default(1)
// @Success 200 {object} HelloResponse
// @Failure 400 {object} ErrorResponse
// @Router /hello [get]
func Hello(c *gin.Context) {
	name := c.Query("name")
	countStr := c.DefaultQuery("count", "1")

	if name == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: "name is required",
		})
		return
	}

	count, err := strconv.Atoi(countStr)
	if err != nil || count < 1 {
		c.JSON(http.StatusBadRequest, ErrorResponse{
			Message: "count must be a positive integer",
		})
		return
	}

	c.JSON(http.StatusOK, HelloResponse{
		Message: "Hello, " + name + "!",
		Count:   count,
	})
}
