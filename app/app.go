package app

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
	"io/fs"
	"log"
	"net/http"
	"os"
	"soar-web/app/api"
	"soar-web/app/route"
	"soar-web/config"
	"soar-web/web"
	"strings"
)

func Run() {

	serverCfg := config.GCfg

	appURL := strings.ToLower(serverCfg.Domain)
	if !strings.HasPrefix(appURL, "http://") && !strings.HasPrefix(appURL, "https://") {
		appURL = fmt.Sprintf("http://%s", serverCfg.Addr)
	}

	r := gin.Default()

	if !config.Debug {
		gin.SetMode(gin.ReleaseMode)
	}
	r.SetTrustedProxies([]string{"127.0.0.1"})
	if serverCfg.Proxy.Enable {
		r.RemoteIPHeaders = serverCfg.Proxy.IPHeader
		r.SetTrustedProxies(serverCfg.Proxy.TrustedProxies)
	} else {
		r.ForwardedByClientIP = false
	}

	// 日志文件配置，如果有日志文件则写入
	if serverCfg.LogFile != "" {
		logfile, err := os.OpenFile(serverCfg.LogFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
		if err != nil {
			fmt.Printf("logfile err %v", err)
		}
		// debug 模式 console 和日志双写
		if config.Debug {
			gin.DefaultWriter = io.MultiWriter(logfile, os.Stdout)
		} else {
			gin.DefaultWriter = io.MultiWriter(logfile)
		}
	}

	r.Use(gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {
		return fmt.Sprintf("[soar-web] %s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
			param.ClientIP,
			param.TimeStamp.Format("2006-01-02 15:04:05"),
			param.Method,
			param.Path,
			param.Request.Proto,
			param.StatusCode,
			param.Latency,
			param.Request.UserAgent(),
			param.ErrorMessage,
		)
	}))
	// 错误恢复
	r.Use(gin.Recovery())

	r.NoMethod(api.HandleNotFound)
	r.NoRoute(api.HandleNotFound)
	// 加载路由
	route.Routes(r)
	r.StaticFile(serverCfg.AdminPathPrefix+"/data/public.rsa", "data/public.rsa")
	StaticFile, _ := fs.Sub(web.WebUI, "webui")
	r.StaticFS(serverCfg.AdminPathPrefix+"/webui", http.FS(StaticFile))

	fmt.Printf("[URL] you can access url %s%s/webui/\n", appURL, serverCfg.AdminPathPrefix)

	//r.GET(serverCfg.AdminPathPrefix, func(ctx *gin.Context) {
	//	ctx.Redirect(302, serverCfg.AdminPathPrefix+"/webui")
	//})
	err := r.Run(serverCfg.Addr)
	if err != nil {
		log.Fatalf("runtime err:%v", err.Error())
	}
}
