#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : soar-api.py.py
# @Author: becivells
# @Date  : 2018/10/31
#@Software : PyCharm
# @Desc  :

import json
import time
import re
import pymysql

from flask import Flask
from flask import request
from flask import redirect
from flask import make_response

from config import HOST
from config import PORT
from config import DEBUG
from core.check import check_env
from core.common import soar_result
from core.common import soar_args_check
from core.common import open_brower
from core.common import parse_dsn
from core.argcrypto import decrypt


app = Flask(__name__)


@app.route('/soar-api',methods=['POST', 'GET'])
def soar():
    arg = request.json
    if  'data' not in arg or 'key' not in arg:
        return json.dumps({
            "result": 'data or key is None',
            "status": True,
            "log": 'error',
        })

    try:
        args = json.loads(decrypt(arg['data'],arg['key']))
    except Exception as e:
        return json.dumps({
            "result": str(e),
            "status": True,
            "log": 'error',
        })
    if DEBUG:
        print (args)

    check = soar_args_check(args)
    if check:
        return check
    result = soar_result(args)

    return result


@app.route('/soar-download',methods=['POST', 'GET'])
def soardownload():
    args = request.values.to_dict()

    if DEBUG:
        print (args)

    check = soar_args_check(args)
    if check:
        return check
    result = soar_result(args)
    map = json.loads(result)
    resp = make_response(map['result'])
    nowTime = time.time()
    timeArray = time.localtime(nowTime)
    otherStyleTime = time.strftime("%Y%m%d%H%M%S", timeArray)
    resp.headers['Content-Type'] = 'application/force-download'
    suffixMap = {'html' : 'html', 'json' : 'json', 'markdown' : 'md'}
    suffix = 'html'
    if 'report-type' in args and args['report-type'] in suffixMap : suffix = suffixMap[args['report-type']]
    resp.headers['Content-Disposition'] = 'filename=soar_%s.%s' % (otherStyleTime, suffix)
    return resp

@app.route('/test-connect',methods=['POST', 'GET'])
def testconnect():
    arg = request.json
    if  'data' not in arg or 'key' not in arg:
        return json.dumps({
            "result": 'data or key is None',
            "status": True,
            "log": 'error',
        })

    try:
        dsn = json.loads(decrypt(arg['data'],arg['key']))['dsn']
    except Exception as e:
        return json.dumps({
            "result": str(e),
            "status": True,
            "log": 'error',
        })

    print(dsn)
    try:
        res = parse_dsn(dsn)
        pymysql.connect(
            host = res['host'],
            port = int(res['port']),
            user = res['user'],
            passwd = res['pwd'],
            db = res['db'],
        )
        status = True
        result = '连接成功'
    except Exception as e:
        status = False
        result = str(e)
    return json.dumps({'result':result, 'status':status})

@app.route('/',methods=['POST', 'GET'])
def index():
    return redirect('/static/index.html')

@app.errorhandler(404)
def f0f(error):
    return json.dumps({
            "result": '404请求不存在', "status": True}
        ),404

@app.errorhandler(Exception)
def error_info(error):
    return json.dumps({
        "result": str(error), "status": False
    })

if __name__ == '__main__':
    # TODO 初始环境检查,包括 tmp，soar 目录是否可读写 soar 不存在自动拉取
    check_env()
    open_brower("http://127.0.0.1:%s"%(PORT))
    app.run(threaded=True,host=HOST,port=PORT)