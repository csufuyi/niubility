# -*- coding:utf-8 -*-

from douban_client import DoubanClient

API_KEY = '020a9c5869bcf26b061fd5093d36d741'
API_SECRET = '1e6e4d4785a8c438'
REDIRECT_URI = 'http://freesz.sinaapp.com/douban'

# 在 OAuth 2.0 中，
# 获取权限需要指定相应的 scope，请注意!!
# scope 权限可以在申请应用的 "API 权限" 查看。

SCOPE = 'douban_basic_common,book_basic_r,book_basic_w'

client = DoubanClient(API_KEY, API_SECRET, REDIRECT_URI, SCOPE)

# 以下方式 2 选 1:
# 1. 引导用户授权
print 'Go to the following link in your browser:' 
print client.authorize_url
code = raw_input('Enter the verification code:')
client.auth_with_code(code)



