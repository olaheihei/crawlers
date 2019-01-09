#coding=utf-8
import requests
import jieba
import json
from os import path
import re
from bs4 import BeautifulSoup

'''
bbs.360che.com/thread-2980014-1-1.html#newbbs_shidahot
bbs.360che.com/forum-97-1.html#newbbs_forum97
thread-2980201-1-1.html
forum-6-2.html
space.php?uid=1859365
https://bbs.360che.com/club-1341-1.html#newbbs_tjclub31
'''

'''
规则：
1、包含thread-, forum-, space.php?uid=, club-等
2、处理为：http://bbs.360che.com/** 的格式
3、爬取页面内容
4、加载词库、分词、判断词性
5、需要的进行记录
6、页面url处理

'''

class 爬虫用到的类(object):
	"""docstring for test_Module"""
	def __init__(self):
		global good_word, bad_word
		jieba.load_userdict(self._语料加载())
		jieba.load_userdict(self._语料加载(要干嘛 = 1))
		jieba.load_userdict(self._语料加载(要干嘛 = 2))
		good_word = self._load_word('good_word')
		bad_word = self._load_word('bad_word')


	def 写东西(self, 内容, 文件名):
		前边的路径 = path.dirname('.')
		后边的路径 = './doc/' + 文件名
		with open(path.join(前边的路径, 后边的路径),'a', encoding='utf-8') as f:
			f.writelines(str(内容)+'\n')


	def 请求用的(self, 网址):
		try:
			return requests.get(网址)
		except:
			return False

	def 返回体转字符串(self, 请求体):
		请求体.encoding = 'gbk'
		文本 = 请求体.text
		return 文本


	def bbs站点用的网址处理(self, 网址):
		if 'bbs.360che.com' not in 网址 and 'bbsedit' not in 网址:
			if '/' not in 网址:
				网址 = '/' + 网址
			网址 = 'bbs.360che.com' + 网址
		if 'http' not in 网址:
			if '//' not in 网址:
				网址 = '//' + 网址
			网址 = 'https:' + 网址
		return 网址


	def 网址整理(self, html的文本):
		美丽体 = BeautifulSoup(html的文本,features="lxml")
		美丽体_body = 美丽体.body
		美丽体_a标签 = 美丽体_body.find_all('a')
		网址集 = []
		for 网址 in 美丽体_a标签:
			if 'thread-' in str(网址):
				网址集.append(self.bbs站点用的网址处理(网址.attrs['href']))
			if 'forum-' in str(网址):
				网址集.append(self.bbs站点用的网址处理(网址.attrs['href']))
			elif 'club-' in str(网址):
				网址集.append(self.bbs站点用的网址处理(网址.attrs['href']))
			elif 'space.php?uid=' in str(网址):
				网址集.append(self.bbs站点用的网址处理(网址.attrs['href']))
		return 网址集


	def 获取内容(self, html的文本):
		美丽体 = BeautifulSoup(html的文本,features="lxml")
		美丽体_body = 美丽体.body
		美丽体_font标签 = 美丽体_body.find_all('font')
		内容 = 美丽体.title.text + '\n'
		for 段落 in 美丽体_font标签:
			if 段落.has_attr('face'):
				内容 = 内容 + 段落.text
		return 内容


	def 获取标题(self, html的文本):
		美丽体 = BeautifulSoup(html的文本,features="lxml")
		return 美丽体.title.text


	def 内容分析(self, 分词列表):
		global good_word, bad_word
		好词 = []
		坏词 = []
		关键词 = self._是否分析(分词列表)
		if 关键词:
			for 词 in 分词列表:
				if 词 in good_word:
					好词.append(词)
				elif 词 in bad_word:
					坏词.append(词)
			if len(好词) or len(坏词):
				if len(好词) > len(坏词):
					return 'good:\n关键词:%s \n好词:%s \n坏词:%s \n' %(关键词, 好词, 坏词) 
				else:
					return 'bad:\n关键词:%s \n好词:%s \n坏词:%s \n' %(关键词, 好词, 坏词) 
			else:
				return False
		else:
			return False


	def _load_File(self, 文件名):
		语料映射 = {'key_word':'key_word.txt', 'good_word':'good_word.txt', 'bad_word':'bad_word.txt'}
		文件路径 = './doc/' + 语料映射[文件名]	
		return 文件路径


	def _语料加载(self, 要干嘛 = 0):
		if 要干嘛 == 0:
			语料干预 = self._load_File('key_word')
		elif 要干嘛 == 1:
			语料干预 = self._load_File('good_word')
		else:
			语料干预 = self._load_File('bad_word')
		return 语料干预


	def 分词(self, 内容):
		内容 = 内容.strip()
		分词列表 = jieba.cut(内容, cut_all=True)
		return self.clean_Format(分词列表)


	def _是否分析(self, 分词列表):
		for 词 in 分词列表:
			if 词 in self._load_word('key_word'):
				return 词
		return False


	def _load_word(self, 文件名):
		语料映射 = {'key_word':'key_word.txt', 'good_word':'good_word.txt', 'bad_word':'bad_word.txt'}
		文件路径 = './doc/' + 语料映射[文件名]	
		词列表 = open(文件路径,encoding ='utf-8').read()
		return [i for i in 词列表.split('\n')]


	def clean_Format(self, words):
		#清理格式、标点
		words_level1 = []
		for i in words:
			if len(i) > 1:
				words_level1.append(i)
		return words_level1



# a = requests.get('https://bbs.360che.com/thread-2980618-1-1.html#newbbs_shitiao')


# a.encoding = 'gbk'
# 文本 = a.text
# 美丽体 = BeautifulSoup(文本,features="lxml")
# 美丽体_body = 美丽体.body
# 美丽体_font标签 = 美丽体_body.find_all('font')
# l = 美丽体.title.text + '\n'
# for i in 美丽体_font标签:
# 	if i.has_attr('face'):
# 		l = l + i.text
# print(l)
# print(l)


# seg_list = jieba.cut("我来到北打发打发发好几封敏捷开发撒复健科发生大幅就卡死范德萨发生犒劳大家分开啦三间房个Ior去问妥if贷款就是氟化氢铵法师的返回空骄傲的说法卡上方啊三点接口返回京清华大学", cut_all=True)
# # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
# for i in seg_list:
# print(i)