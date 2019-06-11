# -*- coding:utf-8 -*-
import flask_restful
from common.utility import custom_abort
from ops.emergency import test
from ops.emergencyDrillNum import emergency_drill_num
from ops.emergencyAlertDetail import emergencyAlertDetail

#from ops.cobblerList import cobblerList
#from ops.cobblerListSync import cobblerListSync

api = flask_restful.Api(catch_all_404s=True)

# 重新定义flask restful 400错误
flask_restful.abort = custom_abort

# test
api.add_resource(test, "/test")
api.add_resource(emergency_drill_num, "/emergencyDrillNum")
api.add_resource(emergencyAlertDetail, "/emergencyAlertDetail")

#api.add_resource(cobblerList, "/cobbler/api/v1.0/cobbler/list")
#api.add_resource(cobblerListSync, "/cobbler/api/v1.0/cobbler/list/sync")
