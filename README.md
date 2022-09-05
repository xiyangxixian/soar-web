# soar-web
基于小米 [soar](https://github.com/XiaoMi/soar) 的开源 sql 分析与优化的 web 图形化工具，支持 soar 配置的添加、修改、复制，多配置切换，配置的导出、导入与导入功能。

![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-1.png?v=2)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-2.png?v=2)
![soar](https://raw.githubusercontent.com/xiyangxixian/soar-web/master/doc/img/example-3.png?v=1)

## 环境需求
项目已经使用 golang 重写
## docker 支持

[![GitHub last commit](https://img.shields.io/github/last-commit/xiaomi/soar?label=soar%20commit)](https://github.com/XiaoMi/soar)
[![GitHub last commit](https://img.shields.io/github/last-commit/xiyangxixian/soar-web?label=soar-web%20commit)](https://github.com/xiyangxixian/soar-web)
[![GitHub last commit](https://img.shields.io/github/last-commit/becivells/soar-web-docker?label=soar-web%20docker%20commit)](https://github.com/Becivells/soar-web-docker)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/becivells/soar-web-docker)](https://github.com/Becivells/soar-web-docker/tags)
[![Docker Pulls](https://img.shields.io/docker/pulls/becivells/soar-web)](https://hub.docker.com/r/becivells/soar-web/)  

地址：[https://hub.docker.com/r/becivells/soar-web/](https://hub.docker.com/r/becivells/soar-web/)   
使用 `github action` 生成docker 镜像并且自动推送给 `DockerHub`

|                  版本                   |                        使用的soar版本                        |                      使用的soar-web版本                      |                           镜像大小                           |
| :-------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| `docker pull becivells/soar-web:latest` | 2021/03/22-[d0d0ce5](https://github.com/XiaoMi/soar/commit/d0d0ce57c9036f7e2e4c5a506e131ce42b332550) | 2020/12/01-[cdde5ef](https://github.com/xiyangxixian/soar-web/commit/cdde5effcbe35c912d53f4c90ae1742887cfbc10) | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/becivells/soar-web/latest) |
| `docker pull becivells/soar-web:2.0.3`  | 2021/03/22-[d0d0ce5](https://github.com/XiaoMi/soar/commit/d0d0ce57c9036f7e2e4c5a506e131ce42b332550) | 2020/12/01-[cdde5ef](https://github.com/xiyangxixian/soar-web/commit/cdde5effcbe35c912d53f4c90ae1742887cfbc10) | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/becivells/soar-web/2.0.3) |
| `docker pull becivells/soar-web:1.0.0`  |                      2019/01/05-g552ccf                      |                      2019/01/05-g552ccf                      | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/becivells/soar-web/1.0.0) |

Dockerfile 见根目录 Dockerfile 文件

```shell script
docker pull becivells/soar-web
docker run -d --name soar-web -p 5077:5077 becivells/soar-web
```

**也可以使用 Dockerfile 自行构建**

```shell script
docker build --no-cache -t soar-web .
```

**访问**

在浏览器上输入 [http://127.0.0.1:5077](http://127.0.0.1:5077/) 进行访问。

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
