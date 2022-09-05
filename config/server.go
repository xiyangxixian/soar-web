package config

import (
	"fmt"
	"os"
	"soar-web/pkg/utils"
	"strings"
	"syscall"

	"github.com/spf13/pflag"
	"github.com/spf13/viper"
)

const (
	AdminPrefixLen = 8
)

// Version is the current versionctl of nuclei
var (
	Version = "unknown"
	Commit  = "unknown"
	Branch  = "unknown"
	Release = "unknown"
)

var GCfg *Config
var YamlVersion = "v0.2"
var YamlVersionList = []string{"v0.1", "v0.2"}
var Debug = false

type Config struct {
	Debug           bool
	Addr            string
	Cert            string
	Key             string
	Domain          string
	Proxy           *ReverseProxy
	LogFile         string
	AdminPathPrefix string
	BinDir          string
}

// ReverseProxy  反向代理配置
type ReverseProxy struct {
	Enable         bool
	IPHeader       []string
	TrustedProxies []string
}

var EtcDir = []string{"soar-web.yaml", "etc/soar-web.yaml", "/etc/soar-web.yaml"}

func SetupConfig() (*Config, error) {

	pflag.String("addr", "127.0.0.1:5077", "server listen addr")
	pflag.String("cert", "", "tls cert file")
	pflag.String("domain", "", "allow domain")
	pflag.String("key", "", "tls key file")
	pflag.String("admin_prefix", "/", "admin prefix")
	pflag.Bool("proxy.enable", false, "proxy")

	pflag.StringArray("proxy.proxy_header", []string{"X-Forwarded-For", "X-Real-IP"}, "proxy")
	pflag.StringArray("proxy.trusted_proxies", []string{"127.0.0.1"}, "proxy")

	pflag.Parse()

	// 优先级按照 /etc/soar-web.yaml, etc/soar-web.yaml, soar-web.yaml 依次降低
	viper.SetConfigName("soar-web")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("/etc/")
	viper.AddConfigPath("etc/")
	viper.AddConfigPath(".")
	viper.AutomaticEnv()
	// 默认配置
	viper.SetDefault("version", YamlVersion)

	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

	if err := viper.BindPFlags(pflag.CommandLine); err != nil {
		return nil, err
	}

	// 如果配置文件不存在则自动生成配置文件
	if !utils.FileInListDir(EtcDir[0], EtcDir) {
		viper.WriteConfigAs(EtcDir[0])
	}
	if err := viper.ReadInConfig(); err != nil {
		return nil, err
	}

	if !utils.StrEqualOrInList(viper.GetString("version"), YamlVersionList) {
		panic("config version not support")
	}
	if viper.GetString("version") != YamlVersion {
		fmt.Printf("配置文件将升级 %s->%s", viper.GetString("version"), YamlVersion)
		viper.Set("version", YamlVersion)
		err := viper.WriteConfig()
		if err != nil {
			return nil, err
		}
	}

	var config = &Config{
		Addr:            viper.GetString("addr"),
		Cert:            viper.GetString("cert"),
		Key:             viper.GetString("key"),
		BinDir:          utils.BinBaseDir(),
		AdminPathPrefix: viper.GetString("admin_prefix"),
		Domain:          viper.GetString("domain"),
		Proxy: &ReverseProxy{
			Enable:         viper.GetBool("proxy.enable"),
			IPHeader:       viper.GetStringSlice("proxy.proxy_header"),
			TrustedProxies: viper.GetStringSlice("proxy.trusted_proxies"),
		},
	}

	return config, nil
}

func check() {

	if utils.FileExist(utils.GetSoarBin()) {
		syscall.Umask(0)
		os.Chmod(utils.GetSoarBin(), 0755)

	} else {
		fmt.Println("soar bin not exist,please install https://github.com/XiaoMi/soar")
		os.Exit(1)
	}

	if !utils.FileExist("data/private.rsa") || !utils.FileExist("data/public.rsa") {
		err := utils.GenRsaKey("data/private.rsa", "data/public.rsa")
		if err != nil {
			fmt.Println("Cannot create certificate file")
			os.Exit(1)
		}
	}

}

func init() {

	utils.MkdirP("data")
	utils.MkdirP("soar-bin")
	var err error
	GCfg, err = SetupConfig()
	if err != nil {
		panic(err)
	}

	check()
}

func ShowInfo() {
	fmt.Printf("Version: %s\n", Version)
	fmt.Printf("Branch: %s\n", Branch)
	fmt.Printf("Commit: %s\n", Commit)
	fmt.Printf("ResDate: %s\n", Release)
}
