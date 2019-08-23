# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from common.log import loggers
import json
import time

logger = loggers()


class healthy(Resource):

  def get(self):
    logger.info("check healthy !")
    return {"status": "UP"}, 200
