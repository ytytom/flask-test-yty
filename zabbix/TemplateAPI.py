#!coding:utf-8
from flask_restful import Resource, reqparse, request
from common.log import loggers
from .ZabbixAPI import Zabbix_Api
from .HostGroupAPI import HostGroupAbout
from .HostAPI import HostAbout
logger = loggers()

parser = reqparse.RequestParser()
parser.add_argument("template_name", type=str, action="append",trim=True, help="host_name cannot be blank!")


class TemplateAbout(Zabbix_Api):


  def GetTemplate(self,auth,*args):
    method = "template.get"
    print(len(args))
    if len(args) == 0:
      params = {
        "output": ["name"],
      }
    else:
      params = {
        "output": ["name"],
        "filter": {
          "name": args
        },
        "selectHosts": ["name"],
      }
    elements = self.common_action(auth, method=method, params=params)
    logger.info("查找所有模板: ,%s", elements, )
    return elements



class GetTemplate(Resource):
  def get(self):
    args = parser.parse_args()
    logger.info("gettinginginginginging args from web  is %s ", args)
    if args.template_name is None:
      Api = Zabbix_Api()
      auth = Api.get_auth()
      template = TemplateAbout()
      AllHost = template.GetTemplate(auth)
    else:
      templatename = args.template_name
      Api = Zabbix_Api()
      auth = Api.get_auth()
      template = TemplateAbout()
      AllHost = template.GetTemplate(auth, *templatename)
      # AllHost = AllHost["name"]

    return {"code": 200, "message": "请求成功", "result": AllHost}


