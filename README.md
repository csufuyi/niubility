# niubility代码库

- 项目计划书见wiki

- 运行方式基于SAE部署,请安装sae本地环境.

- 微信公众号
id:free_shenzhen  
用于测试

## sae环境
浏览器输入：
http://freesz.sinaapp.com

输出：
aha, who are you? welcome to wechat id:free_shenzhen

saecloud deploy 部署代码  
saecloud export 下载代码

## 本地环境  
启动服务器
dev_server.py

浏览器输入：
http://localhost:8080
or 
命令行
curl -v localhost:8080

输出：
aha, who are you? welcome to wechat id:free_shenzhen

## 目的
利用开放平台的api统计牛人趋势信息，分享给其他人使用

## 使用场景 

微信公众号入口操作
- 请求：TED
- 回复：TED牛人列表

- 请求：牛人序号
- 回复：相关的作品[豆瓣]

- 请求：作品名称
- 回复：作品介绍

【非必须】
- 请求：想读相关作品
- 回复：在豆瓣上标记为想读

【非必须】管理员操作
- 请求：更新牛人列表
- 回复：TED牛人信息更新


功能点：
- 微信公众号基于SAE的后台
- 豆瓣api的使用（部分需要OAuth2.0认证）
豆瓣python 封装的api
https://github.com/douban/douban-client
- TED API的使用(网页下载后，分析)
- 微信返回消息的结果组织和展现


已完成：
微信公众号后台搭建
豆瓣API的申请和鉴权测试

待完成：
实际API的使用
返回数据的组织

存在的问题：
在web后台中第三方的token管理和刷新有什么好的建议？
目前计划用DB存储用户的相关数据，并在访问失效以后做刷新。









