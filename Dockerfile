FROM python:3.6-alpine3.8
MAINTAINER  becivells <becivells@gmail.com>
#glib
RUN apk --no-cache add ca-certificates  \
&& wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
&& cd /tmp/&& wget  https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.28-r0/glibc-2.28-r0.apk \
&& apk add glibc-2.28-r0.apk && rm -rf /tmp/*

RUN  apk add --no-cache --virtual .build-deps \
        gcc \
        g++ \
        libffi-dev \
        openssl-dev \
        && wget https://codeload.github.com/xiyangxixian/soar-web/zip/master -O /home/soar-web-master.zip \
        && cd /home/ && unzip soar-web-master.zip&& cd soar-web-master \
        && pip install -r requirement.txt && apk del .build-deps && rm -rf /home/soar-web-master.zip && rm -rf /tmp/*
RUN chmod -R 755 /home/soar-web-master
WORKDIR  /home/soar-web-master
EXPOSE 5077
CMD ["python","/home/soar-web-master/soar-web.py"]