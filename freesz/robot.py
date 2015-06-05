# -*- coding: utf-8 -*-
import json
import re
import traceback

from db import ted_kv
from ted import TED_POPULAR
from db import get_token
from douban import client_wechat
from werobot.robot import werobot
from werobot.utils  import  to_binary
from werobot.session.saekvstorage import SaeKVDBStorage
from xsettings import XCFG

session_storage = SaeKVDBStorage()

robot = werobot.WeRoBot(token=XCFG.TOKEN, enable_session=True,
                        session_storage=session_storage)

@robot.voice
def voicequery(message, session):
    print message.source + ',' +  message.recognition
    return book(message, session)

@robot.text
def log_begin(message, session):
    print message.source + ',' + message.content
    # only care three state
    state = get_state(session)
    if state != 'booklist' and state != 'wishread' and state != 'dnlist':
        set_state(session, None)

@robot.filter("帮助", 'h')
def help(message, session):
    return "输入:\n'大牛'或'dn'获取 TED 最受欢迎演讲者列表\n'豆瓣'或'db'获取豆瓣授权\n'作者或书名[语音]'获取图书信息\n'帮助'或'h'获取帮助"

# get tednamelist saved in ted_kv
@robot.filter("大牛", 'dn')
def speaker(message, session):
    tedstr = ted_kv.get(to_binary(TED_POPULAR))
    retstr = ''
    if None != tedstr:
       speaker_list = json.loads(tedstr)
       if 0 == len(speaker_list):
           return '大牛列表暂时为空'
       for index in range(len(speaker_list)):
           retstr += '[' + str(index) + ']. ' + speaker_list[index] + '\n'
       retstr += u'\n输入序号可以查询大牛著作'
       set_state(session, 'dnlist')
       return retstr
    return "大牛列表暂时还拉不到哦"

# 豆瓣oauth2鉴权   
@robot.filter("豆瓣", 'db')
def douban(message, session):
    guid = message.source
    token = get_token(message, session)
    if None != token:
        try:
            client_wechat.auth_with_token(token)
            client_wechat.book.search('哈哈', '', 0, 1)
            return u"豆瓣授权成功! " + u"公众号id:" + guid + u'豆瓣token:'+token
        except:
            print u"豆瓣token失效了"
    # auth again
    auth_des = u'请点我完成豆瓣授权'
    auth_url =  client_wechat.authorize_url + '&state='+ guid
    auth_html = '<a href="%s">%s</a>' % (auth_url,auth_des)
    return auth_html

# 标记想读 中文正则匹配有问题
@robot.filter(re.compile("\d"))
def wish_read(message, session):
    token = get_token(message, session)
    if (None == token):
        return "输入'豆瓣'完成授权后回到微信"
    client_wechat.auth_with_token(token)
    if get_state(session) == 'booklist' or get_state(session) == 'wishread':
        bookid =  session.get(message.content, 0)
        if 0 == bookid:
            return "输入有误,请重新输入"
        else:
            try:
                client_wechat.book.collection(bookid)
            except:
                return "你收藏过这本书啦!"
            else:
                return "设置想读成功!"
        set_state(session, 'wishread')
    elif get_state(session) ==  'dnlist':
        dnstr =  message.content
        tedstr = ted_kv.get(to_binary(TED_POPULAR))
        retstr = ''
        if None != tedstr:
            speaker_list = json.loads(tedstr)
        dnid = int(dnstr)
        if dnid >= len(speaker_list):
           return '输入有误,请重新输入'
        # change id to keyward
        message.content = speaker_list[dnid]
    
# 根据关键字查书
@robot.text
def book(message, session):
    token = get_token(message, session)
    if (None == token):
        return "输入'豆瓣'完成授权后回到微信"
    client_wechat.auth_with_token(token)
    # get json data from douban 
    try:
        querystr = ''
        if message.type == 'text':
            querystr = message.content
        elif message.type == 'voice':
            querystr = message.recognition
        else:
            return u'暂时没法处理这种输入，我们赶紧查查'
            
        res = client_wechat.book.search(querystr, '', 0, 5)
        res_str = json.dumps(res)
        print res_str
    except Exception, e:
        traceback.print_exc()
        return u"豆瓣授权过期了，请输入'豆瓣'(db)重新授权~"
    count = res['count']
    if count == 0:
        if message.type == 'voice':
            return u"输入的是: '%s' 么？改用文字输入试试吧" %message.recognition
        else:
            return u"没找到啊，修改下关键字试试~"

    ret_str = u'书籍列表:\n'
    if message.type == 'voice':
        ret_str += u"识别的关键词:%s\n" %message.recognition
        
    for i in range(count):
        bookid = res['books'][i]['id']
        #save bookid
        session[str(i)] = bookid
        bookurl = "http://book.douban.com/subject/"+ bookid
        bookauthor = ''
        for index in range(len(res['books'][i]['author'])):
            bookauthor += res['books'][i]['author'][index] + ' '
        ret_str +=  '[' + str(i) + ']' + '.' +res['books'][i]['title']  \
                    + '\n' + bookauthor +  ','   \
                    + res['books'][i]['publisher'] + ',' \
                    + res['books'][i]['pubdate'] \
                    + '\n ' + bookurl + '\n ' + '\n ' 
    ret_str +=  u'输入书的序号0,1,2...可直接标记为想读'
    set_state(session, 'booklist')
    return ret_str 

@robot.subscribe
def subscribe(message):
    return "我是小书童, 很高兴为您服务:\n \n- 输入关键字(书名或作者）查书, 标记为想读, 支持语音哦\n \n- 输入'大牛'或'dn', 查看TED最受欢迎演讲者列表"


def set_state(session, state):
    session["state"] = state
    
def get_state(session):
    return session.get("state", None)
