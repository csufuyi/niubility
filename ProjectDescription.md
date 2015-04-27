# 作品名待定
~ 英文名待定

##简述
- 阳老在开智群中启动了[开智访谈计划],跟大牛面对面,汲取智慧和动力的源泉.陈虎平老师的文章[动力、方向、技术 （之一）](http://weibo.com/p/1001603836012089489228)再次告诉我们,年轻时多接触大师,是一辈子的财富.所以,我们希望对更多大师的思想和著作有所了解.
- 思路:尽量利用**已有的资源**. 
	+ 怎样最快找到各领域的大牛? 一个简单的办法是通过 TED 的 TOP 500 Talks 筛选出大牛. 
	+ 怎样按图索骥找到大牛的著作? 通过 豆瓣和 Google Books 查找.
	+ 怎样通过大牛了解趋势? 通过提取大牛著作的**标签**,通过时间序列分析.
- 所以[作品名]可以:找大牛-列著作-看趋势


##成员
- [free](https://github.com/csufuyi),[教程](http://csufuyi.gitbooks.io/python-startup/content/)
- [弓和箭](https://github.com/badboy315),[教程](http://badboy315.gitbooks.io/pythoncamp0/content/)
- [00](https://github.com/kidult00),[教程](http://kidult00.gitbooks.io/kidult-s-python-book/content/)

##目标
Feature list:

- Feature 1:找大牛
	+ 输入:无
	+ 输出: Ted top 500 talks speaker 列表 (具体数量待定,或者可以选择查看top 100/500/1000)
	+ 问题1:Ted api 没有提供 talks 的播放量,是否暴力抓取?
		* 搜索一通后,发现网站已经有排序列表  http://www.ted.com/talks?sort=popular
	+ 问题2:同一 speaker 的不同 talk 是否需要合并?
		* 需要去重合并

- Feature 2:列著作
	+ 输入(或选择):大牛名字
	+ 输出:
		- 按时间排列的大牛著作
		- 每本著作的标签
		- 每本著作的关注度 (Google books 引用次数([API](https://developers.google.com/books/))? 豆瓣想读/已读数? 再版次数)
	+ 问题1:是否完全匹配名字?
		* 需要精确匹配,是否存在姓和名颠倒情况?是否会省略名字的一部分?
	+ 问题2:书籍有多个作者,按第一作者匹配,还是只要在作者内就可以
		* 先按第一作者匹配,看看搜索的结果数量如何
		

附草图:

![](http://imglf1.ph.126.net/dUBOxmlzq0oxNLpvy1gjOw==/6630619164955302916.jpg)

- Feature 3:看大牛兴趣路径演化
	+ 输入:大牛名字
	+ 输出:	
		- 大牛出现次数最多的标签统计
		- 大牛每10年的标签变化

- Feature 4:看牛群趋势
	+ 输入:领域 (ted 可能没有提供分类数据,得另想办法)或不限领域
	+ 输出:
		- 按时间段查看牛群最关注的标签
		- 按标签查找相应大牛

- Feature 5:标记想读
	+ 输入:著作
	+ 输出:豆瓣图书信息
	+ 其他:标记为想读
	+ 其他1:调用 Rainvoo 的智能购书订单 ? :P

- Feature 6:微信公众号搜索
	+ 输入:在公众号内输入大牛名字(是否支持模糊搜索...)
	+ 输出:大牛的 ted talks 和 豆瓣书籍列表 
	+ 其他:是否可以实现语音输入名字?(微信语音接口目前仅实现普通话识别)

##计划
请腿长补充

### Week0
### Week1
### Week2
### Week3
### Week4