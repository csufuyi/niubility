# Niubility

## 目的
- 群内分享的书，能够在公众号随手查询，并标记为想读  
- 从TED等网站抓取大牛的名字等数据，结合豆瓣展示其作品

## 使用场景
- 微信公众号（id:free_shenzhen）
  输入：豆瓣  
  输出：验证链接（点击后打开验证页面，验证完成后，用户自己回微信）  
  
  输入：作者或书名  
  输出：作品列表（无权限返回鉴权）  

  输入：上面作品列表的ID   
  输出：标记为想读
  
  输入：大牛   
  输出：大牛列表（带作品展示未完成）  
  
  
- web方式（公众号回复关键字在手机端查看）  
  http://freesz.sinaapp.com  
  查询TED大牛统计结果（页面展示未完成）  
  
  http://freesz.sinaapp.com/ted
  TED数据抓取分析存储
  
## 服务端基于sae环境部署
  
-  请安装saecloud工具  
saecloud deploy 部署代码  
saecloud export 下载代码

- 本地环境  
启动服务器
dev_server.py  
浏览器输入：
http://localhost:8080  

## 具体项目计划书见wiki







