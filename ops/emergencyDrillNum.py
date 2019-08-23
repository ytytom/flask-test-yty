# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from common.log import loggers
import json

logger = loggers()

parser = reqparse.RequestParser()
parser.add_argument("drillNum", type=int, default="", trim=True)


class emergency_drill_num(Resource):
  def get(self):
    args = parser.parse_args()
    drillNum = args.drillNum
    logger.info("drillnum get from web is %s ", drillNum)
    return {"status": True, "message": "start task success !", "data": args}
