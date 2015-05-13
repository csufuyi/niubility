# -*- coding:utf-8 -*-

from douban_client import DoubanClient

API_KEY = '020a9c5869bcf26b061fd5093d36d741'
API_SECRET = '2e6e4d4785a8c438'
REDIRECT_URI = 'http://freesz.sinaapp.com/douban'
SCOPE = 'douban_basic_common,book_basic_r,book_basic_w'

client = DoubanClient(API_KEY, API_SECRET, REDIRECT_URI, SCOPE)
print client.authorize_url

