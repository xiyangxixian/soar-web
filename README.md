# soar-web
基于小米 [soar](https://github.com/XiaoMi/soar) 的开源 sql 分析与优化的 web 图形化工具，支持 soar 配置的添加、修改、复制，多配置切换，配置的导出、导入与导入功能。

![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-1.png?v=2)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-2.png?v=2)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-3.png?v=1)

## 环境需求
* python3.x
* Flask
* pymysql
* pycryptodome

python 环境未安装的可参考下面操作：
```
step 1：安装 python

Windows：
去 python 官网下载安装 python3 (已安装可跳过此步骤)

Mac：
brew install python3 python3-pip (如果两个包都有安装可跳过此步骤)

Ubuntu：
sudo apt-get install python3 python3-pip (如果两个包都有安装可跳过此步骤)

CentOS：
sudo yum install python36 python36-pip (如果两个包都有安装可跳过此步骤)

step 2：pip install -r requirement.txt
```
**注**：若 Crypto 模块找不到, 则需要在 python 的依赖库目录 Lib\site-packages 中将 crypto 重命名为 Crypto 。

## 安装与使用
```
下载源码（ Windows 可略过此步骤）：
sudo -y apt-get install wget 或者 sudo yum -y install wget 
wget https://codeload.github.com/xiyangxixian/soar-web/zip/master -O soar-web-master.zip

解压缩（ Windows 可略过此步骤）：
sudo -y apt-get install unzip 或者 sudo yum -y install unzip 
unzip soar-web.zip
cd soar-web-matster

运行启动脚本：
Windows： run.bat
Linux or Mac： bash run.sh

守护进程支持：
启动服务：bash manage.sh start
关闭服务：bash manage.sh stop
重启服务：bash manage.sh restart
```
**注**：当主机上存在多个 python 版本时, 需更改 run.sh, run.bat, manage.sh 中的 python 版本指定为 3.x 的版本运行。

## docker 支持
地址：https://hub.docker.com/r/becivells/soar-web/   
Dockerfile 见根目录 Dockerfile 文件
```
docker pull becivells/soar-web
docker run -d --name soar-web -p 5077:5077 becivells/soar-web
```
**也可以使用 Dockerfile 自行构建**
```
docker build --no-cache -t soar-web .
```

## 访问
在浏览器上输入 http://127.0.0.1:5077 进行访问。

## 配置
如果需要改 IP 地址和端口号, 可在 config.py 中进行修改。

## 功能相关
**关于存储：** 所有的配置都是保存在浏览器 Local Storage 中的，多人之间使用是互不影响的，自己只能看到自己的配置，更换浏览器或者清除浏览器会造成配置丢失。

**关于加密：** 配置信息在发送给服务端前会进行 RSA 和 AES 加密，防止配置信息被窃取。

**配置模板：** 可以添加多数据库连接实例及配置，方便在 sql 评估时切换使用，具体配置项详情见  [https://github.com/XiaoMi/soar/blob/master/doc/config.md](https://github.com/XiaoMi/soar/blob/master/doc/config.md) 。

**数据库连接：** 数据库连接成功后，soar 可以通过表结构提供更正确优质的 sql 评估建议， 配置的正确性决定了 soar 的服务质量。

**线上线下环境问题：** 线上环境作为待 sql 评估环境，soar 在进行 sql 评估时，会根据 sql 语句，从 **线上环境的数据库连接实例** 拷贝数据表到 **测试环境的数据库连接实例**，然后在测试环境下执行 sql 语句进行分析。因此测试环境的数据库连接实例需要有**最高权限**。如果没有最高权限可能造成一些问题，如果没有权限可以启动一个空的 mysql docker 容器作为测试环境。如果仅仅做测试用，可将线上线下环境指定为一样。

**日志等级：** 日志等级为 0 时不打印日志，设置为 1-7 时，会将 soar 产生的日志打印至控制台，按 F12 或右击网页点击审查元素打开调试工具，点击 Console 按钮查看日志。

**soar 版本：** 打开控制台输入：soarVersion()，可查看 soar 版本信息。

## 交流与反馈
* QQ群：881971235
