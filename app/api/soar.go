package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"soar-web/pkg/utils"
)

type SoarParams struct {
	Data string `form:"data" json:"data" binding:"required"`
	Key  string `form:"key" json:"key" binding:"required"`
}

func Version(c *gin.Context) {

	bs, loginfo, err := SoarRun(map[string]string{"version": ""})
	if err != nil {
		errinfo := err.Error()
		Fail(c, errinfo, string(loginfo))
		return
	}
	Success(c, string(bs), string(loginfo))
	return
}

func TestConnect(c *gin.Context) {
	params, err := getParams(c)
	if err != nil {
		errinfo := err.Error()
		Fail(c, err.Error(), errinfo)
		return
	}
	if dsn, ok := params["dsn"]; ok {
		isconn, err := mysqlTest(dsn)
		if isconn {
			Success(c, "测试成功", "")
			return
		}
		errinfo := "测试失败,golang 版本的格式请参考 https://github.com/go-sql-driver/mysql" + err.Error()
		Fail(c, errinfo, errinfo)
	}
	errinfo := "测试失败,golang 版本的格式请参考 https://github.com/go-sql-driver/mysql" + err.Error()
	Fail(c, errinfo, errinfo)
	return
}

func SoarDownload(c *gin.Context) {
	params, err := getParams(c)
	if err != nil {
		Fail(c, err.Error(), "")
		return
	}
	extMap := map[string]string{
		"html":     "html",
		"json":     "json",
		"markdown": "md",
	}

	if _, ok := params["report-type"]; !ok {
		Fail(c, "report-type not found", "")
	}
	if _, ok := extMap[params["report-type"]]; !ok {
		Fail(c, "report-type type is error", "")
	}

	rst, logfile, err := SoarRun(params)
	if err != nil {
		Fail(c, string(rst), string(logfile))
		return
	}

	c.Header("Content-Disposition", fmt.Sprintf("filename=soar_%s.%s", utils.UUID(), extMap[params["report-type"]]))
	c.Data(200, "application/force-download", rst)
	return
}

func SoarAPI(c *gin.Context) {
	params, err := getParams(c)
	if err != nil {
		errinfo := err.Error()
		Fail(c, err.Error(), errinfo)
		return
	}
	rst, loginfo, err := SoarRun(params)
	if err != nil {
		Fail(c, string(rst), string(loginfo))
		return
	}
	Success(c, string(rst), string(loginfo))
	return
}

func getParams(c *gin.Context) (map[string]string, error) {
	var params SoarParams

	if err := c.ShouldBind(&params); err != nil {

		return nil, err
	}
	jsonData, err := DeArgs(params.Data, params.Key)
	if err != nil {
		return nil, err
	}
	v := make(map[string]string)
	err = json.Unmarshal(bytes.Replace(jsonData, []byte{'\x00'}, []byte{' '}, -1), &v)
	if err != nil {
		return nil, err
	}
	return v, nil
}
