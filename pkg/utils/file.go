package utils

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"github.com/gofrs/uuid"
	"os"
	"path/filepath"
	"runtime"
)

const (
	GoOSWindows = "windows"
	GoOSLinux   = "linux"
	GoOSDrawn   = "darwin"
)

func FileExist(path string) bool {
	_, err := os.Lstat(path)
	if err != nil {
		return false
	}
	return !os.IsNotExist(err)
}

func BinBaseDir() string {
	ex, err := os.Executable()
	if err != nil {
		panic(err)
	}
	return filepath.Dir(ex)
}

// StrEqualOrInList string in string list
func StrEqualOrInList(rawStr string, checkStrList []string) bool {
	for _, checkStr := range checkStrList {
		if rawStr == checkStr {
			return true
		}
	}

	return false
}

func FileInListDir(file string, MulDir []string) bool {
	for _, bcfile := range MulDir {
		if FileExists(bcfile) {
			return true
		}
	}
	return false
}

func GetSoarBin() (soarPath string) {
	switch runtime.GOOS {
	case GoOSWindows:
		soarPath = "soar-bin/soar.windows-amd64.exe"
	case GoOSLinux:
		soarPath = "soar-bin/soar.linux-amd64"
	case GoOSDrawn:
		soarPath = "soar-bin/soar.darwin-amd64"
	default:
		soarPath = "soar-bin/soar"
	}
	if !FileExists(soarPath) {
		soarPath = "soar-bin/soar"
	}
	if runtime.GOOS == GoOSWindows {
		soarPath = "soar-bin/soar.exe"
	}
	return
}

func MkdirP(path string) error {
	if !FileExists(path) {
		if err := os.MkdirAll(path, os.ModePerm); err != nil {
			return err
		}
		fmt.Printf("创建文件夹: %v \n", path)
	}
	return nil
}

func UUID() string {
	v4, _ := uuid.NewV4()
	return v4.String()
}

// 判断所给路径文件/文件夹是否存在
func FileExists(path string) bool {
	_, err := os.Stat(path) //os.Stat获取文件信息
	if err != nil {
		return os.IsExist(err)
	}
	return true
}

// 判断所给路径是否为文件夹
func IsDir(path string) bool {
	s, err := os.Stat(path)
	if err != nil {
		return false
	}
	return s.IsDir()
}

//RSA公钥私钥产生
func GenRsaKey(privatefile, publicfile string) error {
	// 生成私钥文件
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return err
	}
	derStream := x509.MarshalPKCS1PrivateKey(privateKey)
	block := &pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: derStream,
	}
	file, err := os.Create(privatefile)
	if err != nil {
		return err
	}
	err = pem.Encode(file, block)
	if err != nil {
		return err
	}
	// 生成公钥文件
	publicKey := &privateKey.PublicKey
	derPkix, err := x509.MarshalPKIXPublicKey(publicKey)
	if err != nil {
		return err
	}
	block = &pem.Block{
		Type:  "PUBLIC KEY",
		Bytes: derPkix,
	}
	file, err = os.Create(publicfile)
	if err != nil {
		return err
	}
	err = pem.Encode(file, block)
	if err != nil {
		return err
	}
	return nil
}
