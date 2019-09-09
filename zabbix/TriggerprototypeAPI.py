from .ZabbixAPI import Zabbix_Api
from flask_restful import Resource, reqparse, request
from common.log import loggers
import json


class TriggerprototypeAPI(Zabbix_Api):
  pass

  def GetTriggerprototype(self,auth,trigger_id):
    method = "triggerprototype.get"
    params = {
      "triggerids": trigger_id,
      "expandExpression": True
      # "selectDependencies": "extend",
      # "selectFunctions": "extend"
      # "monitored": True,
      # "with_triggers": True,
      # "selectApplications": ["name"],
      # "selectTriggers": ["expression", "description", "comments", "status", "state"],
      # "output": ["itemid", "type", "name", "delay", "lastvalue", "state", "status"]
    }
    item_info = self.common_action(auth, method=method, params=params)
    return item_info


class GetTriggerprototype(Resource):
  def get(self):
    pass
  def post(self):
    trigger_id = json.loads(request.data)["trigger_id"]
    Api = Zabbix_Api()
    Triggerprototypeabout = TriggerprototypeAPI()
    auth = Api.get_auth()
    trigger_info = Triggerprototypeabout.GetTriggerprototype(auth, trigger_id)
    return trigger_info
