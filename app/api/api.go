package api

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func TooManyRequests(c *gin.Context, message string) {
	c.JSON(http.StatusTooManyRequests, gin.H{
		"code":    -1,
		"message": message,
	})
}

func Success(c *gin.Context, data interface{}, message string) {
	c.JSON(http.StatusOK, gin.H{
		"status": true,
		"result": data,
		"log":    message,
	})
}

func NotFound(c *gin.Context, message string) {
	c.JSON(http.StatusOK, gin.H{
		"status": false,
		"log":    message,
	})
}

func Fail(c *gin.Context, message, loginfo string) {
	c.JSON(http.StatusOK, gin.H{
		"status": false,
		"result": message,
		"log":    loginfo,
	})
}
