FROM centos:7   
MAINTAINER  becivells <becivells@gmail.com>   

RUN yum install -y epel-release && yum install  -y python-pip git   

RUN git clone https://github.com/xiyangxixian/soar-web.git /opt/soar-web   
RUN cd /opt/soar-web && pip install -r requirement.txt   
RUN chmod -R 755 /opt/soar-web   
EXPOSE 5077   
CMD ["python","/opt/soar-web/soar-web.py"]   
