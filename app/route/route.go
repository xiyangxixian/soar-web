package route

import (
	"github.com/gin-gonic/gin"
	"soar-web/app/api"
	"soar-web/config"
)

func Routes(r *gin.Engine) {
	/* 路由 */
	// 不需要登录登录
	adminPrefix := config.GCfg.AdminPathPrefix
	r.Use(api.RateLimitMiddleware())

	public := r.Group(adminPrefix + "/api")
	public.GET("/soar-version", api.Version)
	public.POST("/test-connect", api.TestConnect)
	public.POST("/soar-download", api.SoarDownload)
	public.POST("/soar-api", api.SoarAPI)

}
