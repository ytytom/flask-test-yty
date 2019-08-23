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
from .AutoCreateHost import Zabbix_Api as Api

parser = reqparse.RequestParser()
parser.add_argument("item_id", type=str, default="", action="append", trim=True)
parser.add_argument("delay", type=str, default="", trim=True)

