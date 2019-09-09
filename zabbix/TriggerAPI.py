from .ZabbixAPI import Zabbix_Api
from flask_restful import Resource, reqparse, request
from common.log import loggers
import json


class TriggerAbout(Zabbix_Api):
  # _triggerid = None
  # _description = None
  # _expression = None
  # _comments = None
  # _flags = None
  # _priority = None
  # _state = None
  # _status = None
  # _tpye = None
  # _value = None
  # _recovery_mode = None
  # _recovery_expression = None
  #
  #
  # def __init__(self,triggerid=_triggerid,description=_description,expression= _expression,comments= _comments,
  #              flags = _flags,priority= _priority,state= _state ,status= _status,tpye=_tpye,value=_value,
  #              recovery_mode=_recovery_mode,recovery_expression=_recovery_expression):
  #   self.triggerid = triggerid
  #   self.description = description
  #   self.expression = expression
  #   self.comments = comments
  #   self.flags = flags
  #   self.priority = priority
  #   self.state = state
  #   self.status = status
  #   self.tpye = tpye
  #   self.value = value
  #   self.recovery_mode = recovery_mode
  #   self.recovery_expression = recovery_expression
  #


  def CreateTrigger(self,):
    pass

  def TriggerGet(self,auth,trigger_id):
    method = "trigger.get"
    params = {
      "triggerids": trigger_id,
      "expandExpression":True,
      "output": ["description","expression","triggerid", "priority","type", "comments", "state", "status"]
      # "output": "extend"
    }
    item_info = self.common_action(auth, method=method, params=params)
    return item_info


  # def TriggerCreate(self,auth,):
  #   pass
  # 主机内trigger的更新



  # DLL trigger的更新？

class GetTrigger(Resource):
  def get(self):
    pass

  def post(self):
    # {
    #   "trigger_id":"10606"
    # }
    pass

    trigger_id = json.loads(request.data)["trigger_id"]
    # print(trigger_id)
    Api = Zabbix_Api()
    triggerabout = TriggerAbout()
    # itemabout = ItemAbout()
    auth = Api.get_auth()
    # item_info = itemabout.UseHostidGetAllItem(auth, *hostids)
    trigger_info = triggerabout.TriggerGet(auth,trigger_id)
    return {"code": 200, "message": "请求成功", "result": trigger_info}
