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

- 请求：【非必须】想读相关作品  
- 回复：在豆瓣上标记为想读

- 请求：【非必须】管理员更新牛人列表
- 回复：TED牛人信息更新


功能点：  
+ 微信公众号基于SAE的后台  
+ 豆瓣api的使用（部分需要OAuth2.0认证）  
+ 豆瓣python 封装的api https://github.com/douban/douban-client
+ TED API的使用(网页下载后，分析)  
+ 微信返回消息的结果组织和展现    








