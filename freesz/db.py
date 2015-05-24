import sae.kvdb
from werobot.utils  import  to_binary
import json
ted_kv = sae.kvdb.Client()

login_kv = sae.kvdb.Client()


# wecaht user info [guid], uid, access token
wechat_kv = sae.kvdb.Client()

# get token saved in wechat_kv
def get_token(message, session):
    guid = message.source
    userstr = wechat_kv.get(to_binary(guid))
    if None != userstr:
       user = json.loads(userstr)
       uid = user['uid']
       token = user['token']
       return token
    return None
