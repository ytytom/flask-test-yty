from .ZabbixAPI import Zabbix_Api
from flask_restful import Resource, reqparse, request
from common.log import loggers
import json

logger = loggers()

class ItemAbout(Zabbix_Api):


  def UseHostidGetAllItem(self,auth,*args):

    method = "item.get"
    params = {
      "hostids": args,
      "monitored": True,
      "with_triggers": True,
      "selectApplications": ["name"],
      "selectTriggers": ["expression","description","comments","status","state"],
      "output":["itemid","type","name","delay","lastvalue","state","status","key_"]
      # "output":["extend"]
    }
    item_info = self.common_action(auth, method=method, params=params)
    return item_info





class GetIteminfo(Resource):
  def get(self):
    pass
  def post(self):
    hostids = json.loads(request.data)["hostid"]
    # print(hostids)
    Api = Zabbix_Api()
    itemabout = ItemAbout()
    auth = Api.get_auth()
    item_info = itemabout.UseHostidGetAllItem(auth,*hostids)
    return {"code":200,"message":"请求成功","result":item_info}
