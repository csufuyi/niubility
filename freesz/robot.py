# -*- coding: utf-8 -*-
import os 
import sys
import sae
import json

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

from werobot.robot import werobot
from werobot.session.saekvstorage import SaeKVDBStorage
from werobot.utils  import * 
from douban_client import DoubanClient
from douban import *

session_storage = SaeKVDBStorage()

# user info [guid], uid, access token
wechat_kv = sae.kvdb.Client()

robot = werobot.WeRoBot(token="freesz", enable_session=True,
                        session_storage=session_storage)

client = DoubanClient(API_KEY, API_SECRET, REDIRECT_URI, SCOPE)

@robot.text
def last(message, session):
    if message.content == u'大牛' or message.content == u'书名': 
        session['last'] = message.content
        
@robot.filter("大牛")
def person(message, session):
    return "大牛列表,请输入TED牛人序号, 待完成"
  
@robot.filter("书名")
def bookname(message, session):
    return "请输入书名"

# 豆瓣oauth2鉴权   
@robot.filter("豆瓣")
def douban(message, session):
    guid = message.source
    token = get_token(message, session)
    # test
    token = None
    if None == token:
        auth_des = u'请点我完成豆瓣授权'
        auth_url =  client.authorize_url + '&state='+ guid
        auth_html = '<a href="%s">%s</a>' % (auth_url,auth_des)
        return auth_html
    else:
        return "auth ok! " + guid + ':'+token

@robot.text
def book(message, session):
    last  = session.get('last', 0)
    print message.content
    if last == u"书名":
        token = get_token(message, session)
        if (None == token):
            return "输入'豆瓣'完成授权后回到微信"
        else:
            client.auth_with_token(token)
            res = client.book.search(message.content, '', 0, 1)
            res_str = json.dumps(res)
            print res_str
            count = res['count']
            if count == 0:
                return "not found"
            else:
                return res['books'][0]['title'] + res['books'][0]['id']

'''
    def test_search_book(self):
                ret = self.client.book.search('坦白')
                        self.assertTrue(isinstance(ret, dict))
                                self.assertTrue(isinstance(ret['books'], list))
                                        self.assertTrue('start' in ret)
                                                self.assertTrue('count' in ret)
                                                        self.assertTrue('total' in ret)

                                                        '''
        
@robot.text
def session_times(message, session):
    count = session.get("count", 0) + 1
    session["count"] = count
    return "请输入'大牛','书名', 你累计发了 %s 条消息" % count

@robot.subscribe
def subscribe(message):
        return "Weclome to niubility! 输入'大牛','书名',有惊喜哦！"

def get_token(message, session):
    guid = message.source
    userstr = wechat_kv.get(to_binary(guid))
    if None != userstr:
       user = json.loads(userstr)
       uid = user['uid']
       token = user['token']
       return token
    return None
