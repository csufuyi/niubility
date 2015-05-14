# -*- coding: utf-8 -*-
import os 
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

from werobot.robot import werobot
from werobot.session.saekvstorage import SaeKVDBStorage

session_storage = SaeKVDBStorage()

robot = werobot.WeRoBot(token="freesz", enable_session=True,
                        session_storage=session_storage)

@robot.filter("TED")
def process():
    return "大牛列表："

@robot.text
def hello(message, session):
    count = session.get("count", 0) + 1
    session["count"] = count
    return "Hello! You have sent %s messages to me" % count

@robot.subscribe
def subscribe(message):
        return "Weclome to niubility! 输入'大牛'"

@robot.handler
def echo(message):
    return  "该怎么回答你呢，还是重新输入'大牛'吧"


