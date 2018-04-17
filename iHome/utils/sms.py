#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from iHome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8aaf070862cc8e560162d2b48fb3042c'

#主帐号Token
accountToken= '9a8017ae088e4b8f973f287be3a4bb42'

#应用Id
appId='8aaf070862cc8e560162d2b4901b0433'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id
class CCP(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            obj = super(CCP,cls).__new__(cls, *args, **kwargs)

            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls._instance = obj
        return cls._instance

    # def __init__(self):
    #     self.rest = REST(serverIP, serverPort, softVersion)
    #     self.rest.setAccount(accountSid, accountToken)
    #     self.rest.setAppId(appId)
    def send_template_sms(self,to,datas,tempid):
        result = self.rest.sendTemplateSMS(to, datas, tempid)
        # print result
        if result.get('statusCode') == '000000':
            return 1
        else:
            return 0


if __name__ == '__main__':
    CCP().send_template_sms('18788331246',['100000','5'],1)


    # obj1 = CCP()

    # obj2 = CCP()
    # print id(obj1)
    # print id(obj2)