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

@robot.filter("正文")
def process():
    return "正文为 a "

@robot.subscribe
def subscribe(message):
        return 'Weclome to niubility!'

@robot.handler
def echo(message):
    return  "该怎么回答你呢，还是重新输入吧"


