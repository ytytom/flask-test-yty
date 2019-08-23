#!coding:utf-8
from flask_restful import Resource, reqparse, request
from common.log import loggers
from .ZabbixAPI import Zabbix_Api
from .HostGroupAPI import HostGroupAbout
logger = loggers()





parser = reqparse.RequestParser()
parser.add_argument("temp_name", type=str, default="CSLC Template OS Linux", trim=True)
parser.add_argument("business_name", type=str, default="", trim=True)
parser.add_argument("host_list", type=str, action="append", trim=True, help="host_list cannot be blank!")
parser.add_argument("host_name", type=str, action="append",trim=True, help="host_name cannot be blank!")




class HostAbout(Zabbix_Api):

  # 获取主机方法
  def host_get(self,auth,*args):

    method = "host.get"

    if len(args) == 0:
      params = {
        "output": ["name", "status", "available"],
        "selectInterfaces": ["ip"],
        "selectParentTemplates": ["name"],

      }
    else:
      host_name = args
      params = {
        "output": [ "name", "status", "available","ip"],
        "filter": {
          "host": host_name
        },
        "selectInterfaces": ["ip"],
        "selectParentTemplates": ["name"],

      }


    host_info = self.common_action(auth,method=method, params=params)

    for i in host_info:
      i["ip"] = i["interfaces"][0]["ip"]


    return host_info


  def Host_relate_group_template(self,auth , group_id, proxy_id, template_id, **hosts_list):
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
      host_info = self.common_action(auth,method=method, params=params)
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
      AllHost = Host.host_get(auth,*host_name)


    return {"code":200,"message":"请求成功","result":AllHost}


class CreateHost(Resource):
  def get(self):


    return 200


class ChangeStatus(Resource):
  def get(self):

    return 200


class JoinGroup(Resource):
  def get(self):

    return 200


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
