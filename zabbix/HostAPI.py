#!coding:utf-8
import json
from flask_restful import Resource, reqparse, request
from common.log import loggers
from .ZabbixAPI import Zabbix_Api
from .HostGroupAPI import HostGroupAbout
from scipy import stats

logger = loggers()

parser = reqparse.RequestParser()
parser.add_argument("temp_name", type=str, default="CSLC Template OS Linux", trim=True)
parser.add_argument("group_name", type=str, default="", trim=True)
parser.add_argument("host_list", type=str, action="append", trim=True, help="host_list cannot be blank!")
parser.add_argument("host_name", type=str, action="append", trim=True, help="host_name cannot be blank!")


class HostAbout(Zabbix_Api):

  # 获取主机方法
  def host_get(self, auth, *args):

    method = "host.get"

    if len(args) == 0:
      params = {
        "output": ["name", "status", "available"],
        "selectInterfaces": ["ip"],
        "selectParentTemplates": ["name"],
        "selectGroups": ["name"],
      }
    else:
      host_name = args
      params = {
        "output": ["name", "status", "available", "ip"],
        "filter": {
          "host": host_name
        },
        "selectInterfaces": ["ip"],
        "selectParentTemplates": ["name"],
        "selectGroups": ["name"],

      }

    host_info = self.common_action(auth, method=method, params=params)

    for i in host_info:
      i["ip"] = i["interfaces"][0]["ip"]
      i["groupname"] = i["groups"][0]["name"]
      i.pop("interfaces")
      i.pop("groups")
      i["hostname"] = i.pop("name")
      i["IPaddress"] = i.pop("ip")

    return host_info

  def Create_Host(self, auth, proxy_id, **kwargs):
    host_name = ""
    host_ip = ""
    method = "host.create"
    params = {
      "host": host_name,
      "proxy_hostid": proxy_id,
      "interfaces": [
        {
          "type": 1,
          "main": 1,
          "useip": 1,
          "ip": host_ip,
          "dns": "",
          "port": "10050"
        }
      ],
      "groups": [
        {
          "groupid": 2
        }
      ],
    }
    hosts_id = []
    for key in kwargs.keys():
      host_ip = kwargs[key]
      params['host'] = key
      params['interfaces'][0]['ip'] = host_ip
      host_info = self.common_action(auth, method=method, params=params)
      logger.info("添加主机过程中 ， %s", host_info)
      hosts_id.append(host_info['hostids'][0])

    return hosts_id



  def UseGroupidGetHost(self, auth, groupid):
    method = "host.get"
    params = {
      "output": ["name", "status", "available", "ip"],
      "groupids": groupid,
      # "filter": {
      #   "groupids": groupid
      # },
      "selectParentTemplates": ["name"],
      "selectInterfaces": ["ip"]
    }
    host_info = self.common_action(auth, method=method, params=params)
    if len(host_info)==0:
      return "该业务组内无机器"
    differntable = []
    for i in host_info:
      i["ip"] = i["interfaces"][0]["ip"]
      i.pop("interfaces")
      differntable.append(len(i["parentTemplates"]))
      i["differntable"] = len(i["parentTemplates"])

    differntableinfo = stats.mode(differntable)[0][0]
    for i in host_info:
      if i["differntable"] == differntableinfo:
        # print(len(i["parentTemplates"]))
        # print(i)
        i["differntable"] = 1
      else:
        i["differntable"] = 0

    return host_info



  def GetUndefindHost(self,auth):
    method = "host.get"
    params = {
      "output": ["name", "status", "available", "ip"],
      "filter": {
        "groupids": "2"
      },
      "selectParentTemplates": ["name"],
      "selectInterfaces": ["ip"]
    }
    host_info = self.common_action(auth, method=method, params=params)
    j = 0
    for i in host_info:
      i["description"] = i["interfaces"][0]["ip"]
      i["title"] = i["name"]
      i["key"] = str(j)
      j += 1
      i.pop("name")
      i.pop("interfaces")
      i.pop("status")
      i.pop("parentTemplates")
      i.pop("hostid")
      if i["available"] == "1":
        i["disabled"] = False
      else:
        i["disabled"] = True
      i.pop("available")
      # i.pop("parentTemplates","interfaces")
    return host_info


  def GetGrouplessHost(self, auth):
    method = "host.get"
    params = {
      "output": ["name", "status", "available", "ip"],
      "filter": {
        "groupids": "2"
      },
      "selectParentTemplates": ["name"],
      "selectInterfaces": ["ip"]
    }
    host_info = self.common_action(auth, method=method, params=params)

    for i in host_info:
      i["ip"] = i["interfaces"][0]["ip"]
      i.pop("interfaces")
      i.pop("parentTemplates")
      # i.pop("parentTemplates","interfaces")
    return host_info

  def UseHostidUpdateGroup(self,auth,group_id,*args):
    method = "host.massupdate"
    params = {
      "hosts": [*args],
      "groups": group_id
    }
    host_info = self.common_action(auth, method=method, params=params)
    return host_info


  # def HostUpdate_G(self,auth,groupid,*args):
  #   method = "host.update"
  #   params = {
  #
  #   }

  def UseHostnameGetHostid(self, auth, *args):
    method = "host.get"
    params = {
      "output": ["hostid","name"],
      "filter": {
        "name": args
      },
      "selectInterfaces": ["ip"]
    }
    logger.info("params is %s",params)
    logger.info("method is %s",method)
    host_info = self.common_action(auth, method=method, params=params)

    hostidlist = []
    for i in host_info:
      i["ip"] = i["interfaces"][0]["ip"]
      hostidlist.append(i["hostid"])
    return host_info

  def UseHostidGetHostname(self, auth, *args):
    method = "host.get"
    params = {
      "filter": {
        "hostid": args
      },
    }
    host_info = self.common_action(auth, method=method, params=params)
    print(host_info)
    hostlist = []
    for i in host_info:
      hostlist.append(i["host"])
    logger.info("XXXXXXXXXXXXXXXXXXXXXX,%s", hostlist)
    return hostlist

  def Host_relate_group_template(self, auth, group_id, proxy_id, template_id, **hosts_list):
    # def Host_relate_group_template(self,*hosts_list, **kwargs):
    host_name = ""
    host_ip = ""
    method = "host.create"
    params = {
      "host": host_name,
      "proxy_hostid": proxy_id,
      "interfaces": [
        {
          "type": 1,
          "main": 1,
          "useip": 1,
          "ip": host_ip,
          "dns": "",
          "port": "10050"
        }
      ],
      "groups": [
        {
          "groupid": group_id
        }
      ],
      "templates": [
        {
          "templateid": template_id
        }
      ]
    }
    hosts_id = []
    for key in hosts_list.keys():
      host_ip = hosts_list[key]
      params['host'] = key
      params['interfaces'][0]['ip'] = host_ip
      host_info = self.common_action(auth, method=method, params=params)
      logger.info("添加主机过程中 ， %s", host_info)
      hosts_id.append(host_info['hostids'][0])

    tmp_len = len(hosts_id)
    tmp_str = "成功添加%s台机器" % (tmp_len)

    return tmp_str






class GetAllHost(Resource):
  def get(self):
    args = parser.parse_args()
    logger.info("gettinginginginginging args from web  is %s ", args)
    if args.host_name is None:
      Api = Zabbix_Api()
      Host = HostAbout()
      auth = Api.get_auth()
      AllHost = Host.host_get(auth)
    else:
      host_name = args.host_name
      Api = Zabbix_Api()
      Host = HostAbout()
      auth = Api.get_auth()
      AllHost = Host.host_get(auth, *host_name)

    return {"code": 200, "message": "请求成功", "result": AllHost}


class UseGroupidGetHost(Resource):
  def get(self):
    pass

  def post(self):
    # {
    #   "group_id":"2"
    # }
    Api = Zabbix_Api()
    logger.info("Create an API instance")
    auth = Api.get_auth()
    logger.info("Get an auth")
    Groupid = json.loads(request.data)["group_id"]
    print(Groupid)
    hostaction = HostAbout()
    AllHost = hostaction.UseGroupidGetHost(auth, Groupid)
    if AllHost =="该业务组内无机器":
      return {"code": 201, "message": AllHost, "result": []}
    else:
      return {"code": 200, "message": "请求成功", "result": AllHost}



class GetUndefindHost(Resource):
  def get(self):
    Api = Zabbix_Api()
    logger.info("Create an API instance")
    auth = Api.get_auth()
    logger.info("Get an auth")
    hostaction = HostAbout()
    AllHost = hostaction.GetUndefindHost(auth)
    return {"code": 200, "message": "请求成功", "result": AllHost}

class GetGrouplessHost(Resource):
  def get(self):
    Api = Zabbix_Api()
    logger.info("Create an API instance")
    auth = Api.get_auth()
    logger.info("Get an auth")
    hostaction = HostAbout()
    AllHost = hostaction.GetGrouplessHost(auth)
    return {"code": 200, "message": "请求成功", "result": AllHost}


class CreateHost(Resource):
  def get(self):
    Api = Zabbix_Api()
    logger.info("Create an API instance")
    auth = Api.get_auth()
    logger.info("Get an auth")
    args = parser.parse_args()
    host_list = args.host_list
    host_dir = {}
    for i in host_list:
      temp = i.split(":")
      host_dir[temp[0]] = temp[1]

    proxy_name = "Zabbix proxy"
    proxy_id = Api.Get_proxy_id(auth, proxy_name)
    logger.info("according to %s ,create the proxy_id is %s", proxy_name, proxy_id)

    hostaction = HostAbout()
    logger.info("useing hostabout")

    hostinfo = hostaction.Create_Host(auth, proxy_id, **host_dir)
    logger.info("according to %s, %s", host_dir, hostinfo)

    hostname = hostaction.UseHostidGetHostname(auth, *hostinfo)

    # 返回请求成功的机器Ip
    return {"code": 200, "message": "请求成功", "result": hostname}


class ChangeStatus(Resource):
  def get(self):
    return 200

class HostJoinGroup(Resource):
  def get(self):
    pass
  def post(self):
    # {
    #   "group_id": "1",
    #   "hosts": ["xx", "xx", "xxx"]
    # }
    group_id = json.loads(request.data)["group_id"]
    hosts = json.loads(request.data)["hosts"]
    print(hosts)
    Api = Zabbix_Api()
    hostids = []

    for i in hosts:
      hostid = {}
      hostid["hostid"]=i
      hostids.append(hostid)
    logger.info("Create an API instance")
    auth = Api.get_auth()
    logger.info("Get an auth")
    hostgroup = HostGroupAbout()
    hostaction = HostAbout()
    hostupdate = hostaction.UseHostidUpdateGroup(auth, group_id, *hostids)
    hg_information = hostgroup.UseGroupidGetName(auth,group_id)
    host_id = hostupdate["hostids"]
    hostname = hostaction.UseHostidGetHostname(auth,*host_id)

    #建群组
    # group_id = hostgroupabout.Hostgroup_add(auth,group_name)
    #拿hostid
    # hostaction = HostAbout()
    # host_id = hostaction.UseHostnameGetHostid(auth,*hosts)
    # for i in host_id:
    #   i.pop("name")
    #   i.pop("interfaces")
    #   i.pop("ip")
    #
    # hostupdate = hostaction.UseHostidUpdateGroup(auth,group_id,*host_id)
    # hostupdate_hostid = hostupdate["hostids"]
    # successhostname = hostaction.UseHostidGetHostname(auth,*hostupdate_hostid)
    # return {"group_id":group_id,"hostupdate":hostupdate}
    return {"code": 200, "message": "请求成功", "result": {"groupname":hg_information,"hostupdate":hostname}}



class JoinGroup(Resource):
  def get(self):
    return 200
  def post(self):
    print(request.data)
    group_name = json.loads(request.data)["group_name"]
    hosts = json.loads(request.data)["hosts"]
    Api = Zabbix_Api()
    logger.info("Create an API instance")
    auth = Api.get_auth()
    logger.info("Get an auth")
    hostgroupabout = HostGroupAbout()
    hostaction = HostAbout()
    groupid = hostgroupabout.Hostgroup_ifhas(auth,group_name)
    if groupid == 0:
      return {"code": 400, "message": "请求失败", "result": "群组以存在"}
    else:
      host_info = hostaction.UseHostidUpdateGroup(auth,groupid,*hosts)
      return host_info



class LinkTemplate(Resource):
  def get(self):
    return 200



class UseHostGroupCreate(Resource):
  def get(self):
    Api = Zabbix_Api()
    logger.info("Create an API instance")

    auth = Api.get_auth()
    logger.info("Get an auth")
    args = parser.parse_args()
    template = args.temp_name

    template_id = Api.Get_template_id(auth, template)
    logger.info("according to %s ,get the id is %s ", template, template_id)

    hostgroupabout = HostGroupAbout()
    logger.info("useing hostgroupabout")

    group_name = args.business_name

    host_list = args.host_list
    host_dir = {}
    for i in host_list:
      temp = i.split(":")
      host_dir[temp[0]] = temp[1]

    group_id = hostgroupabout.Hostgroup_add(auth, group_name)
    logger.info("according to %s ,create the group_id is %s", group_name, group_id)

    proxy_name = "Zabbix proxy"
    proxy_id = Api.Get_proxy_id(auth, proxy_name)
    logger.info("according to %s ,create the proxy_id is %s", proxy_name, proxy_id)

    hostaction = HostAbout()
    logger.info("useing hostabout")

    hostinfo = hostaction.Host_relate_group_template(auth, group_id, proxy_id, template_id, **host_dir)

    logger.info("according to %s, %s", host_dir, hostinfo)
    return hostinfo
