FROM xiyangxixian/soar-web:base

MAINTAINER Docker xiyangxixian <2554758802@qq.com>

RUN apt-get install -y --no-install-recommends git

RUN pip3 install Flask pymysql"]

EXPOSE 5077
CMD ["python3 /soarweb/soar-web.py"]
