#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: becivells
# @Date  : 2018/11/2
#@Software : PyCharm
# @Desc  :

import os

# WEB 服务器地址
HOST = '0.0.0.0'

# WEB 服务器端口
PORT = 5077

# 根目录
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# 临时目录
TMP_DIR = BASE_DIR + os.sep + 'tmp' + os.sep
SOAR_PATH = BASE_DIR + os.sep + 'soar' + os.sep

# 是否打开浏览器
IS_OPEN_BROWESER = True  # True False

# 私钥文件
RSA_PRIVATE_DIR = BASE_DIR + os.sep + 'data' + os.sep + 'private.rsa'
# 公钥文件
RSA_PUBLIC_DIR = BASE_DIR + os.sep + 'static' + os.sep + 'data' + os.sep + 'public.rsa'

# 是否打开调试模式
DEBUG = False

# 多值定义需要使用英文,隔开方式返回
MUL_SOAR_ARGS = [    'ignore-rules','explain-warn-access-type',
                     'table-allow-charsets', 'rewrite-rules',
                     'explain-warn-select-type', 'explain-warn-access-type'
                     'explain-warn-extra', 'explain-warn-scalability',
                     'table-allow-engines'
                    # 'blacklist' # blacklist单独处理以换行符为分隔符号
                 ]

# SOAR_RUN_TIMEOUT = 5  # soar 执行超时后直接强制退出 暂时不用

SOAR_NOT_USE_ARGS = ['version','log-output','verbose','print-config']

SOAR_ARGS = {
    "allow-drop-index": None,
    "allow-online-as-test": None,
    "alsologtostderr": None,
    "blacklist": str,
    # "config": str,  # 配置文件服务器端自动生成
    "conn-time-out": int,
    "delimiter": str,
    "drop-test-temporary": None,
    "dry-run": None,
    "explain": None,
    "explain-format": str,
    "explain-max-filtered": float,
    "explain-max-keys": int,
    "explain-max-rows": int,
    "explain-min-keys": int,
    "explain-sql-report-type": str,
    "explain-type": str,
    "explain-warn-access-type": str,
    "explain-warn-extra": str,
    "explain-warn-scalability": str,
    "explain-warn-select-type": str,
    "ignore-rules": str,
    "index-prefix": str,
    "list-heuristic-rules": None,
    "list-report-types": None,
    "list-rewrite-rules": None,
    "list-test-sqls": None,
    "log-level": int,
    "log-output": str,
    "log_backtrace_at": "value",
    "log_dir": str,
    "logtostderr": None,
    "markdown-extensions": int,
    "markdown-html-flags": int,
    "max-column-count": int,
    "max-distinct-count": int,
    "max-group-by-cols-count": int,
    "max-in-count": int,
    "max-index-bytes": int,
    "max-index-bytes-percolumn": int,
    "max-index-cols-count": int,
    "max-index-count": int,
    "max-join-table-count": int,
    "max-pretty-sql-length": int,
    "max-query-cost": int,
    "max-subquery-depth": int,
    "max-total-rows": int,
    "max-varchar-length": int,
    "online-dsn": str,
    "only-syntax-check": None,
    "print-config": None,
    "profiling": None,
    "query": str,
    "query-time-out": int,
    "report-css": str,
    "report-javascript": str,
    "report-title": str,
    "report-type": str,
    "rewrite-rules": str,
    "sampling": None,
    "sampling-statistic-target": int,
    "show-last-query-cost": None,
    "show-warnings": None,
    "spaghetti-query-length": int,
    "sql-max-length-errors": int,
    "sql-max-length-ui": int,
    "stderrthreshold": "value",
    "table-allow-charsets": str,
    "table-allow-engines": str,
    "test-dsn": str,
    "trace": None,
    "unique-key-prefix": str,
    # "v": "value",  # 无用配置
    "verbose": None,
    "version": None,
    # "vmodule": "value",  #无用配置
}
