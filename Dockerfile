#
# BUILD FOR SOAR-WEB
# AUTHOR: <rovast@163.com>
#

FROM ubuntu:18.04

# dependencies required for running "phpize"
# (see persistent deps below)
ENV SOAR_WEB_PACKAGE_DEPS \
		git \
		python \
		python-pip

# persistent / runtime deps
RUN apt-get update && apt-get install -y \
		$SOAR_WEB_PACKAGE_DEPS \
	--no-install-recommends && rm -r /var/lib/apt/lists/*

RUN git clone https://github.com/rovast/soar-web.git /opt/soar-web
RUN cd /opt/soar-web && pip install -r requirement.txt   
RUN chmod -R 755 /opt/soar-web   
EXPOSE 5088
CMD ["python","/opt/soar-web/soar-web.py"]
