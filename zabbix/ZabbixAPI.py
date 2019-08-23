#!coding:utf-8
from common.log import loggers
import json
import requests

logger = loggers()

mysql_user = 'zabbix'
mysql_host = '172.20.13.201'
mysql_pass = 'zabbix'
zabbix_user = 'Admin'
zabbix_pass = 'zabbix'
zabbix_api_url = 'http://172.20.13.203/zabbix/api_jsonrpc.php'



class Zabbix_Api(object):


  def __init__(self):#zabbix 定义访问url 和headers
    self.url = zabbix_api_url
    self.headers = {'Content-Type': 'application/json'}

  def get_auth(self):
    # 这个也没有毛病
    self.data = {
      "jsonrpc": "2.0",
      "method": "user.login",
      "params": {
        "user": zabbix_user,
        "password": zabbix_pass
      },
      "id": 1,
      "auth": None
    }
    # 没找到调用别个函数的self.data 这里先写一遍
    response = requests.post(self.url, data=json.dumps(self.data), headers=self.headers)
    response_auth = json.loads(response.text)
    logger.info("get_auth: get the auth is OK，auth is %s", response_auth['result'])
    return response_auth['result']



  def common_action(self,auth, **kwargs):
  #传参定义，使用字典类型
  #定义zabbix的data 后面除了auth除外的方法，都使用这个定义的模板
    self.data = {
      "jsonrpc": "2.0",
      "method": "user.login",
      "params": {
        "user": zabbix_user,
        "password": zabbix_pass
      },
      "id": 1,
      "auth": None
    }

    logger.info("what's action wanner to do %s，\n **kwargs  is :%s , ", kwargs['method'],kwargs)
    #每次传参的参数有哪些？
    self.data['method'] = kwargs['method']
    self.data['params'] = kwargs['params']
    self.data['auth'] = auth
    return self.post_action(self.data)



  def post_action(self, data):
    #通用post函数
    response = requests.post(self.url, data=json.dumps(data), headers=self.headers)
    response_data = json.loads(response.text)
    logger.info(" ..response_data %s", response_data)
    return response_data['result']



  def Get_template_id(self,auth ,template_name):
    #用template name 来得到template id
    method = "template.get"
    params = {
      "output": "extend",
      "filter": {
        "host": template_name
        }
      }
    template_info = self.common_action( auth,method=method, params=params)
    current_template_id = template_info[0]['templateid']
    return current_template_id



  def Get_proxy_id(self,auth, proxy_name ):
    #用proxy name 拿到proxy id
    method = "proxy.get"
    params = {
      "output": "extend",
      "selectInterface": "extend",
      "filter": {
        "host": [proxy_name, ]
      }
    }
    template_info = self.common_action( auth,method=method, params=params)
    proxy_id = template_info[0]["proxyid"]
    return proxy_id








