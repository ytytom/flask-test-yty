#!coding:utf-8
from flask_restful import Resource, reqparse, request
from common.log import loggers
from .ZabbixAPI import Zabbix_Api

logger = loggers()



parser = reqparse.RequestParser()
parser.add_argument("temp_name", type=str, default="CSLC Template OS Linux", trim=True)
parser.add_argument("business_name", type=str, default="", trim=True)
parser.add_argument("host_list", type=str, action="append", trim=True, help="host_list cannot be blank!")
parser.add_argument("host_name", type=str, action="append",trim=True, help="host_name cannot be blank!")
parser.add_argument("group_name", type=str, action="append",trim=True, help="host_name cannot be blank!")




class HostGroupAbout(Zabbix_Api):
  #有关主机组的方法

  def get_hostgroup(self,auth,*args):
    #查找所有主机群组
    method = "hostgroup.get"
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
    logger.info("查找所有主机组: ,%s", elements, )
    return elements




  def Hostgroup_ifhas(self, auth, hgname):
    #依据群组名返回是否存在主机组
    method = "hostgroup.get"
    params = {
      "output": "extend",
      "filter": {
        "name": hgname
      }
    }
    elements = self.common_action(auth,method=method, params=params)
    ele_num = len(elements)
    logger.info("判断当前主机组是否存在的信息 (0代表不存在)%s , 对应的主机名称为: ,%s", ele_num,hgname)
    return ele_num


  def Hostgroup_add(self,  auth,hgname):

    #传创建主机组的动作
    #只有hgname一个参数
    method = "hostgroup.create"
    params = {
      "name": hgname
    }

    flags = self.Hostgroup_ifhas(auth,hgname)
    #判断主机组是否存在
    if flags == 0:
      try:
        hg_information = self.common_action(auth,method=method, params=params)
        tmp = hg_information['groupids'][0]
        return tmp
      except Exception as e:
        return e

    else:
      tmp = "the name of hostgroup has exist"
    return tmp



class GetAllHostGroup(Resource):
  def get(self):
    args = parser.parse_args()
    logger.info("gettinginginginginging args from web  is %s ", args)
    if args.group_name is None:
      Api = Zabbix_Api()
      auth = Api.get_auth()
      host_group = HostGroupAbout()
      AllHost = host_group.get_hostgroup(auth)
    else:
      host_name = args.group_name
      Api = Zabbix_Api()
      host_group = HostGroupAbout()
      auth = Api.get_auth()
      AllHost = host_group.get_hostgroup(auth, *host_name)
      # AllHost = AllHost["name"]

    return {"code":200,"message":"请求成功","result":AllHost}



class CreateGroup(Resource):
  def get(self):
    return 200

class LinkTemplate_G(Resource):
  def get(self):
    return 200
