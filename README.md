# soar-web
基于小米 [soar](https://github.com/XiaoMi/soar) 的开源 sql 分析与优化的 WEB 图形化工具，支持 soar 配置的添加、修改、复制，多配置切换，配置的导出、导入与导入功能。

![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-1.png?v=1)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-2.png?v=1)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-3.png?v=1)

## 环境需求
* python2.7 or python3.x
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
step 1 sudo yum install python3 python3-pip (如果两个包都有安装可跳过此步骤)
setp 2 pip install Flask
setp 3 pip install pymysql
```


## 安装与使用
```
Windows： run.bat
Linux or Mac： sh run.sh
```

然后在浏览器上输入 http://127.0.0.1:5077 进行访问

如果需要改IP地址和端口号, 可在 config.py 中进行修改
