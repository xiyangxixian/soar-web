# soar-web
基于小米 [soar](https://github.com/XiaoMi/soar) 的开源 sql 分析与优化的 WEB 图形化工具，支持 soar 配置的添加、修改、复制，多配置切换，配置的导出、导入与导入功能。

![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-1.png?v=2)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-2.png?v=1)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-3.png?v=1)

## 环境需求
* python3.x
* Flask
* pymysql

Python 环境未安装的可参考下面操作：
```
Windows：
step 1 去 python 官网下载安装 python3 (已安装可跳过此步骤)
setp 2 pip install Flask
setp 3 pip install pymysql

Mac：
step 1 brew install python3 python3-pip (如果两个包都有安装可跳过此步骤)
setp 2 pip install Flask
setp 3 pip install pymysql

Ubuntu：
step 1 sudo apt-get install python3 python3-pip (如果两个包都有安装可跳过此步骤)
setp 2 pip install Flask
setp 3 pip install pymysql

CentOS：
step 1 sudo yum install python36 python36-pip (如果两个包都有安装可跳过此步骤)
setp 2 pip install Flask
setp 3 pip install pymysql
```

## 安装与使用
```
下载源码（Windows 可略过此步骤）：
sudo -y apt-get install wget 或者 sudo yum -y install wget 
wget https://codeload.github.com/xiyangxixian/soar-web/zip/master -O soar-web.zip 

解压缩（Windows 可略过此步骤）：
sudo -y apt-get install unzip 或者 sudo yum -y install unzip 
unzip soar-web.zip
cd soar-web-matster

运行启动脚本
Windows： run.bat
Linux or Mac： bash run.sh

守护进程支持：
启动服务：bash manage.sh start
关闭服务：bash manage.sh stop
重启服务：bash manage.sh restart

注：当主机上存在多个 python 版本时, 需自行更改 run.sh, run.bat, manage.sh 中的 python 版本指定为 3.x 以上的版本运行。
```

## docker 支持
地址：https://hub.docker.com/r/becivells/soar-web/   
Dockerfile 见根目录 Dockerfile 文件
```
docker pull becivells/soar-web
docker run -d --name soar-web -p 5077:5077 becivells/soar-web
```

## 访问
在浏览器上输入 http://127.0.0.1:5077 进行访问

## 配置
如果需要改IP地址和端口号, 可在 config.py 中进行修改
