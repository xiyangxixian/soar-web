FROM ubuntu:18.04
MAINTAINER  xiyangxixian <2554758802@qq.com>

RUN apt-get update
RUN apt-get install -y --no-install-recommends --no-install-suggests python3 python3-pip git
RUN git clone https://github.com/xiyangxixian/soar-web.git /soar-web
RUN ln -s /usr/bin/python3 //usr/bin/python
RUN pip3 install setuptools
RUN cd /soar-web && pip3 install -r requirement.txt
RUN chmod -R 777 /soar-web
EXPOSE 5077
CMD ["python3","/soar-web/soar-web.py"]