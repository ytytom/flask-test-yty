# -*- coding:utf-8 -*-
import flask_restful
from common.utility import custom_abort
from ops.emergency import test
from ops.emergencyDrillNum import emergency_drill_num
from ops.emergencyAlertDetail import emergencyAlertDetail
# from zabbix.AutoCreateHost import AutoCreateHost
# from zabbix.AddItemTragger import AddItemTragger

from common.healthy import healthy
from zabbix.HostGroupAPI import GetAllHostGroup,LinkTemplate_G,CreateGroup

from zabbix.HostAPI import GetAllHost,CreateHost,JoinGroup,LinkTemplate,ChangeStatus,UseGroupidGetHost,\
  GetUndefindHost,HostJoinGroup,GetGrouplessHost

from zabbix.TemplateAPI import GetTemplate
# from ops.cobblerList import cobblerList
# from ops.cobblerListSync import cobblerListSync

api = flask_restful.Api(catch_all_404s=True)

# 重新定义flask restful 400错误
flask_restful.abort = custom_abort

# test
api.add_resource(healthy,"/health")
#健康检查
api.add_resource(test, "/test")
# api.add_resource(AutoCreateHost, "/zabbix/AutoCreateHost")
# api.add_resource(AddItemTragger, "/zabbix/AddItemTragger")
api.add_resource(emergency_drill_num, "/emergencyDrillNum")
api.add_resource(emergencyAlertDetail, "/emergencyAlertDetail")

##group about##
api.add_resource(GetAllHostGroup,"/group/GetGroup")
api.add_resource(LinkTemplate_G,"/group/LinkTemplate_G")
api.add_resource(CreateGroup,"/group/CreateGroup")




##host about##
api.add_resource(GetAllHost,"/host/GetHost")
api.add_resource(GetUndefindHost,"/host/GetUndefindHost")
api.add_resource(UseGroupidGetHost,"/host/UseGroupidGetHost")
api.add_resource(CreateHost,"/host/CreateHost")
api.add_resource(JoinGroup,"/host/JoinGroup")
api.add_resource(LinkTemplate,"/host/LinkTemplate")
api.add_resource(ChangeStatus,"/host/ChangeStatus")
api.add_resource(HostJoinGroup,"/host/HostJoinGroup")
api.add_resource(GetGrouplessHost,"/host/GetGrouplessHost")




# api.add_resource(cobblerList, "/cobbler/api/v1.0/cobbler/list")
# api.add_resource(cobblerListSync, "/cobbler/api/v1.0/cobbler/list/sync")
# api.add_resource(UseHostGroupCreate,"/UseHostGroupCreate")


##模板类
api.add_resource(GetTemplate,"/template/GetTemplate")
