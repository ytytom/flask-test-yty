#!coding:utf-8
from flask_restful import Resource, reqparse, request
from common.log import loggers
import sys
import json
import time
import requests
import re
import string
import uuid

# from .ZabbixAPI import Zabbix_Api as Api

parser = reqparse.RequestParser()
parser.add_argument("host_name", type=str, default="", action="append", trim=True)

# parser.add_argument("business_name", type=str, default="", required=True, trim=True)
# parser.add_argument("host_list", type=str, required=True, action="append", trim=True, help="host_list cannot be blank!")

logger = loggers()












# class AddItemTragger(Resource):

#   def get(self):
#     zabbix = Api()
#     auth = zabbix.get_auth()
#     args = parser.parse_args()
#     logger.info("args from web is %s", args)
#     # host_name = args.host_name
#     hostinformation = zabbix.host_get(auth)
#     return hostinformation







