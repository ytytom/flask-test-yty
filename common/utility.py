# -*- coding:utf-8 -*-
from flask import abort, jsonify
#from common.db import DB
#import uuid
from common.log import loggers
from datetime import datetime



logger = loggers()




# 重新定义flask restful 400错误
def custom_abort(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        if kwargs:
            for key in kwargs["message"]:
                parameter = key
        else:
            parameter = "unknown"
        abort(jsonify({"status": False, "message": "The specified %s parameter does not exist" % parameter}))
    return abort(http_status_code)

# 本地时间转UTC
def local_to_utc(local):
    local_format = "%Y-%m-%d %H:%M:%S"
    local_tm = datetime.strptime(local, local_format)
    utc = datetime.utcfromtimestamp(local_tm.timestamp())
    return utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# UTC转本地时间
def utc_to_local(utc):
    utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    utc_tm = datetime.strptime(utc, utc_format)
    local_tm = datetime.fromtimestamp(0)
    utc_dtm = datetime.utcfromtimestamp(0)
    offset = local_tm - utc_dtm
    local = utc_tm + offset
    return local.strftime("%Y-%m-%d %H:%M:%S")


