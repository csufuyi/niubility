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

from douban import client 

app = Bottle()

@app.get("/")
def checkSignature():
     # 你在微信公众平台上设置的TOKEN
     token = "freesz"
     wechat = WechatBasic(token=token)
     signature = request.GET.get('signature', None)  
     timestamp = request.GET.get('timestamp', None)
     nonce = request.GET.get('nonce', None)
     if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return request.GET.get('echostr', None);
     return "aha, who are you? welcome to wechat id:free_shenzhen"

@app.post('/')
def post():
    # 用户的请求内容 (Request 中的 Body)
    str_xml = request.body.read()
    xml = etree.ElementTree.fromstring(str_xml)
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
    # 构造填充返回给用户的xml 
    res_text  = body_text % (touser, fromuser,  int(time.time()), text, wechat)
    token = "freesz"  # 你在微信公众平台上设置的TOKEN
    wechat = WechatBasic(token=token)

    # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
    wechat.parse_data(res_text)

    # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
    message = wechat.get_message()
    response = None
    if message.type == 'text':
        response = wechat.response_text("你的openid:%s, 我才刚出生，欢迎教我" % (fromuser))
    elif message.type == 'image':
        response = wechat.response_text(u'图片')
    else:
        response = wechat.response_text(u'未知')
    print response
    return response


@app.get("/douban")
def douban_oauth():
     code = request.GET.get('code', None)
     print code
     global client 
     client.auth_with_code(code)
     print client.token_code
     return "oauth begin"

@app.post('/douban')
def douban_oauth_sucess():
    print "after post"
    global client 
    print client.token_code
    

application = sae.create_wsgi_app(app)

