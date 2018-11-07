#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : soar-api.py.py
# @Author: becivells
# @Date  : 2018/10/31
#@Software : PyCharm
# @Desc  :

import json

from flask import Flask
from flask import request
from flask import redirect

from config import HOST
from config import PORT
from config import DEBUG
from config import IS_OPEN_BROWESER
from core.common import soar_result
from core.common import soar_args_check
from core.common import open_brower


app = Flask(__name__)


@app.route('/soar-api',methods=['POST', 'GET'])
def soar():
    args = request.values.to_dict()

    if DEBUG:
        print (args)

    check = soar_args_check(args)
    if check:
        return check
    result = soar_result(args)

    return result

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
    if DEBUG:
        result = str(error)
    else:
        result = '500 error'
    return json.dumps({
        "result": result, "status": False}
    )

if __name__ == '__main__':
    # TODO 初始环境检查,包括 tmp，soar 目录是否可读写 soar 不存在自动拉取
    if IS_OPEN_BROWESER: open_brower("http://127.0.0.1:%s"%(PORT))
    app.run(threaded=True,host=HOST,port=PORT)
