package api

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func HandleNotFound(c *gin.Context) {
	c.String(http.StatusNotFound, "404 page not found")
}
