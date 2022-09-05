package api

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"database/sql"
	"encoding/base64"
	"encoding/pem"
	"errors"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"os"
	"os/exec"
	"regexp"
	"soar-web/pkg/utils"
	"strings"
)

var SoarArgsAlowList = map[string]bool{}

func runCmd(args ...string) ([]byte, error) {

	ecmd := exec.Command(utils.GetSoarBin(), args...)
	return ecmd.CombinedOutput()
}

// 初始化
func init() {
	by, _ := runCmd("--help")
	soarRg := regexp.MustCompile("(?m)^\\s+(-([^\\s]*))")
	argsList := soarRg.FindAllString(string(by), -1)
	for _, arg := range argsList {
		SoarArgsAlowList[strings.TrimSpace(arg)] = true
	}
}

func SoarRun(argsMap map[string]string) ([]byte, error) {

	var argsList = []string{}
	for key, arg := range argsMap {
		key := "-" + strings.TrimSpace(key)
		if rst, ok := SoarArgsAlowList[key]; !(ok && rst) {
			errinfo := "请检查soar程序是否可以正常运行，如果正常是soar-web 不允许的参数: " + arg
			return []byte(errinfo), errors.New(errinfo)
		} else {
			if arg == "" {
				argsList = append(argsList, fmt.Sprintf("%s", key))
			} else {
				argsList = append(argsList, fmt.Sprintf("%s=%s", key, arg))
			}

		}
	}
	ecmd := exec.Command(utils.GetSoarBin(), argsList...)
	return ecmd.CombinedOutput()
}

func RSA_Decrypt(cipherText []byte, path string) ([]byte, error) {
	//打开文件
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	//获取文件内容
	info, _ := file.Stat()
	buf := make([]byte, info.Size())
	file.Read(buf)
	//pem解码
	block, _ := pem.Decode(buf)
	//X509解码
	privateKey, err := x509.ParsePKCS1PrivateKey(block.Bytes)
	if err != nil {
		return nil, err
	}
	//对密文进行解密
	plainText, err := rsa.DecryptPKCS1v15(rand.Reader, privateKey, cipherText)
	if err != nil {
		return nil, err
	}
	//返回明文
	return plainText, nil
}

func PKCS5UnPadding(origData []byte) []byte {
	length := len(origData)
	unpadding := int(origData[length-1])
	fmt.Printf("origData:%s,origData_len:%d,unpadding:%v,length:%vl-u:%d,\n", origData, len(origData), unpadding, length, length-unpadding)
	if unpadding > length {
		return origData
	}
	return origData[:(length - unpadding)]
}
func AesDecrypt(crypted, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}
	blockSize := block.BlockSize()

	blockMode := cipher.NewCBCDecrypter(block, key[:blockSize])
	origData := make([]byte, len(crypted))
	blockMode.CryptBlocks(origData, crypted)
	//origData = PKCS5UnPadding(origData)
	return origData, nil
}

// CBCDecrypt AES-CBC 解密
func AesDecrypt1(ciphertext, key []byte) ([]byte, error) {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("cbc decrypt err:", err)
		}
	}()

	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	ciphercode := ciphertext

	iv := ciphercode[:aes.BlockSize]        // 密文的前 16 个字节为 iv
	ciphercode = ciphercode[aes.BlockSize:] // 正式密文

	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(ciphercode, ciphercode)

	plaintext := ciphercode // ↓ 减去 padding
	return plaintext[:len(plaintext)-int(plaintext[len(plaintext)-1])], nil
}

func DeArgs(data, key string) ([]byte, error) {
	rsaCrypted, err := base64.StdEncoding.DecodeString(key)
	if err != nil {
		return nil, err
	}
	plainText, err := RSA_Decrypt(rsaCrypted, "data/private.rsa")
	if err != nil {
		return nil, err
	}
	aescr, err := base64.StdEncoding.DecodeString(data)
	if err != nil {
		return nil, err
	}
	bb, err := AesDecrypt(aescr, plainText)
	if err != nil {
		return nil, err
	}
	return bb, nil
}

func mysqlTest(dsn string) (bool, error) {
	db, err := sql.Open("mysql", dsn)

	if err != nil {
		return false, err
	}
	defer db.Close()
	err = db.Ping()
	if err != nil {
		return false, err
	}
	return true, nil
}
