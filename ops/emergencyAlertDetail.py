# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from common.log import loggers
import json

logger = loggers()

parser = reqparse.RequestParser()
parser.add_argument("drillNum", type=int, default="", required=True, trim=True)
parser.add_argument("Node", type=str, trim=True)
parser.add_argument("NodeAlias", type=str, trim=True)
parser.add_argument("Severity", type=int, trim=True)
parser.add_argument("Summary", type=str, trim=True)
parser.add_argument("CSL_ComponentType", type=str, trim=True)
parser.add_argument("CSL_Component", type=str, trim=True)
parser.add_argument("CSL_SubComponent", type=str, trim=True)

AlertDeatil = {
  '1': (['001'], ['002', 3], ['004'], ['005'], ['006', '0061', '0062', '0063'], ['007'], ['008'])
}


class emergencyAlertDetail(Resource):
  def get(self):
    args = parser.parse_args()
    logger.info("args from web is %s", args)
    drillNum = args.drillNum
    logger.info("Drillnum from web is %s", drillNum)
    for key, value in AlertDeatil.items():
      if key == str(drillNum):
        logger.info("AlertDeatil from dict  is %s", AlertDeatil[key])
        return AlertDeatil[key]

  def post(self):
    pass
