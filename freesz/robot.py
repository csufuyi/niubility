# -*- coding: utf-8 -*-
import json
import re

from db import ted_kv
from ted import TED_POPULAR
from db import get_token
from douban import client_wechat
from werobot.robot import werobot
from werobot.utils  import  to_binary
from werobot.session.saekvstorage import SaeKVDBStorage

session_storage = SaeKVDBStorage()

robot = werobot.WeRoBot(token="freesz", enable_session=True,
                        session_storage=session_storage)

@robot.text
def log_begin(message):
    print message.source + ',' + message.content

# get tednamelist saved in ted_kv
@robot.filter("大牛")
def speaker(message, session):
    print TED_POPULAR
    tedstr = ted_kv.get(to_binary(TED_POPULAR))
    retstr = ''
    if None != tedstr:
       speaker_list = json.loads(tedstr)
       if 0 == len(speaker_list):
           return '大牛列表暂时为空'
       for index in range(len(speaker_list)):
           retstr += str(index) + ' ' + speaker_list[index] + '\n'
       return retstr
    return "大牛列表暂时还拉不到哦"

# 豆瓣oauth2鉴权   
@robot.filter("豆瓣")
def douban(message, session):
    guid = message.source
    token = get_token(message, session)
    if None != token:
        try:
            client_wechat.auth_with_token(token)
            return u"豆瓣授权成功! " + u"公众号id:" + guid + u'豆瓣token:'+token
        except:
            print message.source + "token失效了"
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
    else:
        client_wechat.auth_with_token(token)
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
 
# 根据关键字查书
@robot.text
def book(message, session):
    token = get_token(message, session)
    if (None == token):
        return "输入'豆瓣'完成授权后回到微信"

    # get json data from douban 
    try:
        client_wechat.auth_with_token(token)
        res = client_wechat.book.search(message.content, '', 0, 3)
        res_str = json.dumps(res)
        print res_str
    except:
        return u"往豆瓣的路上，网络出问题了，稍后再试吧~"
    count = res['count']
    if count == 0:
        return u"没找到啊，修改下关键字试试~"

    ret_str = u'作品列表:\n'
    for i in range(count):
        bookid = res['books'][i]['id']
        #save bookid
        session[str(i)] = bookid
        bookurl = "http://book.douban.com/subject/"+ bookid
        bookauthor = ''
        for index in range(len(res['books'][i]['author'])):
            bookauthor += res['books'][i]['author'][index] + ' '
        ret_str +=  str(i) + ',' +res['books'][i]['title'] + ',' \
                    + bookauthor +  ','   \
                    + res['books'][i]['publisher'] + ',' \
                    + res['books'][i]['pubdate'] + ',' \
                    + 'pages:' + res['books'][i]['pages'] + ','\
                    + bookurl + '\n ' 
    ret_str +=  u'\n输入书序号0,1,2可标记为想读'
    return ret_str 

@robot.text
def session_times(message, session):
    count = session.get("count", 0) + 1
    session["count"] = count
    return "你累计发了 %s 条消息" % count

@robot.subscribe
def subscribe(message):
    return "欢迎来到Niubility! 输入任意关键字(书名或作者）查书，输入'大牛'有惊喜哦！"

@robot.handler
def log_end(message):
    print message.source + ',' + message.content
    return "不好意思，我还不知道怎么处理这个..."
