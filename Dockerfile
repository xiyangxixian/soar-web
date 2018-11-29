FROM centos:7
MAINTAINER  becivells <becivells@gmail.com>

RUN yum install -y epel-release && yum install  -y python-pip wget unzip

RUN wget https://codeload.github.com/xiyangxixian/soar-web/zip/master -O /opt/soar-web-master.zip
RUN cd /opt/ && unzip soar-web-master.zip&& cd soar-web-master && pip install -r requirement.txt
RUN chmod -R 755 /opt/soar-web-master  && yum clean all && rm -rf /tmp/*
EXPOSE 5077
CMD ["python","/opt/soar-web-master/soar-web.py"]