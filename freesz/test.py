# -*- coding: utf-8 -*-
import sys
import time
from subprocess import Popen
from xsettings import XCFG

if __name__ == "__main__":
    if 2 != len(sys.argv):
        print """ Usage::
        $ python CLI.py [指令]
        """
    else:
        TPL_TEXT='''<xml>
        <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
        <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
        <CreateTime>%(tStamp)s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%(content)s]]></Content>
        </xml>'''

        toUser = XCFG.AS_SRV
        fromUser = XCFG.AS_USR

        tStamp = int(time.time())
        content = sys.argv[1]
        xml = TPL_TEXT % locals()

        cmd = "curl -d '%s' http://localhost:8080/api/"% xml         #完成测试命令编辑
        print cmd
        Popen(cmd, shell=True, close_fds=True)                                        #执行
