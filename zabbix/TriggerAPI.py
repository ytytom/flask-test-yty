from .ZabbixAPI import Zabbix_Api

class Trigger(Zabbix_Api):
  _triggerid = None
  _description = None
  _expression = None
  _comments = None
  _flags = None
  _priority = None
  _state = None
  _status = None
  _tpye = None
  _value = None
  _recovery_mode = None
  _recovery_expression = None


  def __init__(self,triggerid=_triggerid,description=_description,expression= _expression,comments= _comments,
               flags = _flags,priority= _priority,state= _state ,status= _status,tpye=_tpye,value=_value,
               recovery_mode=_recovery_mode,recovery_expression=_recovery_expression):
    self.triggerid = triggerid
    self.description = description
    self.expression = expression
    self.comments = comments
    self.flags = flags
    self.priority = priority
    self.state = state
    self.status = status
    self.tpye = tpye
    self.value = value
    self.recovery_mode = recovery_mode
    self.recovery_expression = recovery_expression

  def TriggerGet(self,itemid,**kwargs):

    pass



