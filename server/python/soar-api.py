#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : soar-api.py.py
# @Author: becivells
#@Contact : becivells@gmail.com
# @Date  : 2018/10/31
#@Software : PyCharm
# @Desc  :
import os
import json
import uuid
from flask import Flask,request
from config import soar_args
from config import BASE_DIR
from core.parse import req_parse2cmd_parse
from core.common import runcmd
app = Flask(__name__)


@app.route('/soar-api',methods=['POST', 'GET'])
def hello_world():
    args = request.values.to_dict()

    for arg,v in args.items():
        if arg not in soar_args:
            return json.dump({'error':'参数错误','status':True})
    if 'query' not in args:
        return json.dumps({'error':'请输入sql','status':True})
    else:
        _tmpfile = BASE_DIR + os.sep + 'tmp' + os.sep + str(uuid.uuid1())
        with open(_tmpfile,'a') as f:
            f.write(args['query'])
    args['query']=_tmpfile
    args['report-type']='markdown'
    cmd_line = req_parse2cmd_parse(args)
    try:
        return json.dumps({"result":runcmd(cmd_line).decode('utf8'),"status":True})
    except Exception as e:
        return json.dumps({'error':str(e),'status':True})
    finally:
        os.remove(_tmpfile)





if __name__ == '__main__':
    app.run()
