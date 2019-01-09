#coding=utf-8
from g_module import 爬虫用到的类


进行测试的站点set = set(['http://bbs.360che.com'])
需要爬的网址set = set()
已爬网址的set = set()
单次网址记录set = set()
爬虫对象 = 爬虫用到的类()
已分析文章set = set()


def 舆情监控_站点发散():
	global 需要爬的网址set
	global 单次网址记录set
	global 已爬网址的set
	for 网址 in 已爬网址的set:
		try:
			需要爬的网址set.remove(网址)
		except:
			pass
	for 网址 in 单次网址记录set:
		if 网址 not in 已爬网址的set:
			需要爬的网址set.add(网址)
	单次网址记录set.clear()


def 统计():
	global 需要爬的网址set,已爬网址的set,单次网址记录set,已分析文章set
	print('进行测试的站点：%s'%进行测试的站点set)
	print('需要爬的网址set：%s'%len(需要爬的网址set))
	print('已爬网址的set:%s'%len(已爬网址的set))
	print('单次网址记录set:%s'%len(单次网址记录set))
	print('已分析文章set:%s\n'%len(已分析文章set))


def 舆情监控_内容分析(html文本):
	内容定性 = 爬虫对象.内容分析(爬虫对象.分词(爬虫对象.获取内容(html文本)))
	return 内容定性


def 舆情监控_日志记录(标题, 地址, 内容定性):
	日志 = 标题 + ':' + 地址 + '\n' + 内容定性
	爬虫对象.写东西(日志, 'hehe.txt')


def 舆情监控_内容爬虫():
	global 已爬网址的set
	global 需要爬的网址set
	global 单次网址记录set
	global 已分析文章set
	for 网址 in 需要爬的网址set:
#		单次网址记录set.upda te(爬虫对象.网址整理(爬虫对象.返回体转字符串(爬虫对象.请求用的(网址))))
		响应体 = 爬虫对象.请求用的(网址)
		html文本 = 爬虫对象.返回体转字符串(响应体)
		if 响应体:
			if 'thread' in 网址:
				舆情结果 = 舆情监控_内容分析(html文本)
				if 舆情结果:
					舆情监控_日志记录(爬虫对象.获取标题(html文本), 网址, 舆情结果)
				已分析文章set.add(网址)
			else:
				单次网址记录set.update(爬虫对象.网址整理(html文本))
			已爬网址的set.add(网址)
		else:
			已爬网址的set.add(网址)
		统计()


def 舆情监控_1级站点爬取():
	global 需要爬的网址set
	global 已爬网址的set
	for 网址 in 进行测试的站点set:
		需要爬的网址set.update(爬虫对象.网址整理(爬虫对象.返回体转字符串(爬虫对象.请求用的(网址))))
		已爬网址的set.add(网址)



舆情监控_1级站点爬取()
while 1:
	舆情监控_内容爬虫()
	舆情监控_站点发散()
	if len(已分析文章set) > 100:
		爬虫对象.写东西(已分析文章set, 'run_log.txt')
	break
