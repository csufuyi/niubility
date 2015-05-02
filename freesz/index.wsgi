# -*- coding:utf-8 -*-
import sae
import os
import sys
import time

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

from bottle import Bottle, debug, run, request
from wechat_sdk.basic import WechatBasic
from xml import etree
from xml.etree import ElementTree

app = Bottle()

@app.route('/')
def hello():
    print 'hello'
    return "hello log"

@app.get("/")
def checkSignature():
     token = "freesz"  # 你在微信公众平台上设置的TOKEN
     wechat = WechatBasic(token=token)
     signature = request.GET.get('signature', None)  
     timestamp = request.GET.get('timestamp', None)
     nonce = request.GET.get('nonce', None)
     if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return request.GET.get('echostr', None);
     return "no check"

'''    
     token = ""  # 你在微信公众平台上设置的TOKEN
     signature = request.GET.get('signature', None)  # 拼写不对害死人那，把signature写成singnature，直接导致怎么也认证不成功
     timestamp = request.GET.get('timestamp', None)
     nonce = request.GET.get('nonce', None)
     echostr = request.GET.gext('echostr', None)
     tmpList = [token, timestamp, nonce]
     tmpList.sort()
     tmpstr = "%s%s%s" % tuple(tmpList)
     hashstr = hashlib.sha1(tmpstr).hexdigest()
     if hashstr == signature:
         return echostr
     else:
         return "wws:indentify error"
'''

@app.post('/')
def post():
    # 用户的请求内容 (Request 中的 Body)
    str_xml = request.body.read()
    xml = etree.ElementTree.fromstring(str_xml)#进行XML解析
    wechat = xml.find("Content").text
    text = xml.find("MsgType").text
    fromuser = xml.find("FromUserName").text
    touser = xml.find("ToUserName").text
   
    body_text = """
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <MsgId>6038700799783131222</MsgId>
    </xml>
    """
    response_text  = body_text % (touser, fromuser,  int(time.time()), text, wechat)
    print response_text
    token = "freesz"  # 你在微信公众平台上设置的TOKEN
    # 实例化 wechat
    wechat = WechatBasic(token=token)

    # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
    wechat.parse_data(response_text)
    # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
    message = wechat.get_message()
    response = None
    if message.type == 'text':
        response = wechat.response_text(u'文字')
    elif message.type == 'image':
        response = wechat.response_text(u'图片')
    else:
        response = wechat.response_text(u'未知')
    print response
    return response

    # 对签名进行校验
application = sae.create_wsgi_app(app)

