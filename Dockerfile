FROM golang:1.16-alpine as builder
ENV GOROOT="/usr/local/go"
ENV GOPATH="/root/go"
ENV PATH="${PATH}:${GOROOT}/bin"
ENV PATH="${PATH}:${GOPATH}/bin"

RUN apk update && apk --no-cache add gcc git make
RUN mkdir  -p ${GOPATH}/src/github.com/XiaoMi/ && git clone -b dev https://github.com/XiaoMi/soar.git ${GOPATH}/src/github.com/XiaoMi/soar
RUN cd ${GOPATH}/src/github.com/XiaoMi/soar &&  CGO_ENABLED=0 make &&mv bin/soar /root/

FROM python:3.6-alpine3.8
MAINTAINER  becivells <becivells@gmail.com>

RUN  apk add --no-cache --virtual .build-deps \
        gcc \
        g++ \
        libffi-dev \
        openssl-dev \
        && wget https://codeload.github.com/xiyangxixian/soar-web/zip/master -O /home/soar-web-master.zip \
        && cd /home/ && unzip soar-web-master.zip&& cd soar-web-master \
        && pip install -r requirement.txt && apk del .build-deps \
        &&  rm -rf /home/soar-web-master.zip && rm -rf /tmp/* && rm -rf /home/soar-web-master/soar/*

COPY --from=builder /root/soar /home/soar-web-master/soar/soar.linux-amd64
RUN chmod -R 755 /home/soar-web-master/soar/
WORKDIR  /home/soar-web-master
EXPOSE 5077
CMD ["python","/home/soar-web-master/soar-web.py"]
