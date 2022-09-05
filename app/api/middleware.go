package api

import (
	"github.com/gin-gonic/gin"
	"github.com/juju/ratelimit"
	"time"
)

func RateLimitMiddleware() func(c *gin.Context) {
	bucket := ratelimit.NewBucketWithQuantum(time.Second, 100, 100) ////初始100，每秒放出100
	return func(c *gin.Context) {
		// 如果取不到令牌就中断本次请求返回 rate limit...
		if bucket.TakeAvailable(1) < 1 {
			TooManyRequests(c, "请求太过频繁请稍后再试")
			c.Abort()
			return
		}
		c.Next()
	}
}
