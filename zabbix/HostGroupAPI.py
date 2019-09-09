#!coding:utf-8
from flask_restful import Resource, reqparse, request
from common.log import loggers
from .ZabbixAPI import Zabbix_Api
import json

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
        "sortfield": "groupid",
        "excludeSearch": True, #匹配到除了Linux servers外的群组
        "search":{
          "name": "Linux servers"
        },
        "selectHosts": ["name"],
      }
    else:
      params = {
        "output": ["name"],
        "filter": {
          "name": args
        },
        "selectHosts": ["name"],
        "sortfield": "groupid",
        # "sortfield": "groupid"
      }
    elements = self.common_action(auth, method=method, params=params)
    logger.info("查找所有主机组: ,%s", elements, )
    for i in elements:
      i["hosts"] = len(i["hosts"])
    return elements




  def Hostgroup_ifhas(self, auth, hgname):
    #依据群组名返回是否存在主机组
    method = "hostgroup.get"
    params = {
      "output": "groupid",
      "filter": {
        "name": hgname
      }
    }
    elements = self.common_action(auth,method=method, params=params)

    ele_num = len(elements)

    logger.info("判断当前主机组是否存在的信息 (0代表不存在)%s , 对应的主机名称为: ,%s", ele_num,hgname)

    if ele_num == 0:
      return "0"
    else:
      groupid = elements[0]["groupid"]
      return groupid


  def Hostgroup_add(self,  auth,group_name):


    method = "hostgroup.create"
    params = {
      "name": group_name
    }

    hg_information = self.common_action(auth,method=method, params=params)
    tmp = hg_information['groupids'][0]
    print(tmp)
    return tmp

  def UseGroupidGetName(self,auth,group_id):
    method = "hostgroup.get"
    params = {
      "output": ["name",],
      "groupids": group_id
    }
    hg_information = self.common_action(auth, method=method, params=params)
    groupname = hg_information[0]["name"]
    return groupname

  def UseGroupnameGetid(self,auth,hgname):
    method = "hostgroup.get"
    params= {
      "output": "groupid",
      "filter": {
        "name": hgname
      }
    }
    flags = self.Hostgroup_ifhas(auth, hgname)

    try:
      hg_information = self.common_action(auth, method=method, params=params)
      tmp = hg_information['groupids'][0]
      return tmp
    except Exception as e:
      return e


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

  def post(self):

    hostgroups = json.loads(request.data)["group_name"]
    # hostgroups = request.form["group_name"]
    print(hostgroups)
    Api = Zabbix_Api()
    host_group = HostGroupAbout()
    auth = Api.get_auth()
    AllHost = host_group.get_hostgroup(auth, hostgroups)
    return  {"code":200,"message":"请求成功","result":AllHost}




class LinkTemplate_G(Resource):
  def get(self):
    return 200


class CreateGroup(Resource):
  def get(self):
    pass

  def post(self):
    Api = Zabbix_Api()
    auth = Api.get_auth()
    group_name = json.loads(request.data)["group_name"]
    groupablout = HostGroupAbout()
    group_info = groupablout.Hostgroup_ifhas(auth, group_name)
    if group_info == "0":
      create_group = groupablout.Hostgroup_add(auth,group_name)
      return {"code": 200, "message": "请求成功", "result":{"group_id":create_group,"group_name":group_name}}
    else:
      # return  {"code":200,"message":"请求成功","result":group_info}
      return {"code": 400, "message": "请求失败", "result": "业务组重名"}
