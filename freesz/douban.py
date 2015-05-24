# -*- coding:utf-8 -*-
from douban_client import DoubanClient

API_KEY = '020a9c5869bcf26b061fd5093d36d741'
API_SECRET = '2e6e4d4785a8c438'
REDIRECT_URI = 'http://freesz.sinaapp.com/douban'
SCOPE = 'douban_basic_common,book_basic_r,book_basic_w'

client_wechat = DoubanClient(API_KEY, API_SECRET, REDIRECT_URI, SCOPE)

LOGIN_API_KEY = '09009bd8ce37c64f1b01d38a6aa752ed'
LOGIN_API_SECRET = 'd2cc229aa607ae60'
LOGIN_REDIRECT_URI = 'http://freesz.sinaapp.com/login'
LOGIN_SCOPE = 'douban_basic_common,book_basic_r,book_basic_w'


client_login = DoubanClient(LOGIN_API_KEY, LOGIN_API_SECRET, LOGIN_REDIRECT_URI, LOGIN_SCOPE)