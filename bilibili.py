#!/usr/bin/env python
# coding=utf-8

from __future__ import division
from collections import defaultdict
from collections import Counter

import sys
import re
import json
import getopt
import requests
import config
import time
import copy
import os



class Danmu():

	"""Download Danmu and save as ssa file"""

	def __init__(self):
		self.comment_url = 'http://comment.bilibili.com/'
		self.script_info = config.SCRIPT_INFO
		self.v4_styles = config.V4_STYLES
		self.events = config.EVENTS
		self.item = ('[Script Info]','[v4 Styles] ','[Events]')

		
	def time_format(self, time, types):
		time = float(time)
		if types == '1':
			endtime = time + 11
		else:
			endtime = time + 4
		start = str(int(time/3600))+':'+str(int(time/60))+':'+str(int(time%60))+'.'+str(time%60-int(time%60))[2:4]
		end = str(int(endtime/3600))+':'+str(int(endtime/60))+':'+str(int(endtime%60))+'.'+str(endtime%60-int(endtime%60))[2:4]
		return (start, end)
		

	def get_danmu(self, url):
		print '\033[1;36m喵娘正在启动 \033[1;32m【 OK 】\033[0m'
		self.danmu_dict = {}
		content = requests.get(url).content
		print '\033[1;36m解析視頻地址 \033[1;32m【 OK 】\033[0m'
		if len(content) < 10000:
			return 0
		pat0 = re.compile(r'bili-cid=(.*)&bili-aid')
		bili_cid = re.findall(pat0, content)
		if bili_cid:
			pass
		else:
			pat1 = re.compile(r'cid=(.*)&aid')
			bili_cid = re.findall(pat1, content)
		comment_xml = requests.get(''.join([self.comment_url, bili_cid[0], '.xml'])).content
		comment_pat = re.compile(r'<d p="(.*)">(.*)</d>')
		for m, n in re.findall(comment_pat, comment_xml):
			danmu_detail = m.split(',')
			danmu_content = danmu_detail[0]+','+danmu_detail[1]+','+danmu_detail[3]+','+n 
			self.danmu_dict[danmu_detail[7]] = danmu_content.split(',')
		len_danmu = [len(p[3]) for q,p in self.danmu_dict.iteritems()]
		counts = Counter(len_danmu)
		self.danmu_counts = sorted(counts.most_common(20))
		print '\033[1;36m全舰弹幕装填 \033[1;32m......\033[0m'



	def deal_danmu(self):
		self.style = {}
		white_style = self.v4_styles.get('Style')[0]
		color_style = self.v4_styles.get('Style')[1]
		center_style = self.v4_styles.get('Style')[2]
		centerw_style = self.v4_styles.get('Style')[3]
		rolling_events = self.events.get('rolling')
		static_events = self.events.get('static')
		deal_dict = copy.deepcopy(self.danmu_dict)
		count_list = [i[0] for i in self.danmu_counts]
		del_list = [single_id for single_id, content in deal_dict.iteritems() if len(content[3]) not in count_list]
		map(lambda x: deal_dict.pop(x), del_list)
		self.danmu_list = []
		for m,n in deal_dict.iteritems():
			time_tup = self.time_format(n[0], n[1])
			if n[2] != '16777215' and n[1] == '1':
				self.style[n[2]] = color_style.format(style = n[2], color_code = n[2])
			elif n[2] == '16777215' and n[1] == '1':
				self.style['16777215'] = white_style.format(style = '16777215')
			elif n[2] == '16777215' and n[1] != '1':
				self.style['center16777215'] = centerw_style.format(style = 'center16777215')
			elif n[2] != '16777215' and n[1] != '1':
				self.style['center'+n[2]] = center_style.format(style = 'center'+n[2], color_code = n[2])
			if n[1] == '1' and n[2] == '16777215':
				self.danmu_list.append(rolling_events.format(start_time = time_tup[0],end_time = time_tup[1],style = '16777215',text = n[3]))
			elif n[1] == '1' and n[2] != '16777215':
				self.danmu_list.append(rolling_events.format(start_time = time_tup[0],end_time = time_tup[1],style = n[2], text = n[3]))
			elif n[1] != '1' and n[2] == '16777215':
				self.danmu_list.append(static_events.format(start_time = time_tup[0], end_time = time_tup[1],style = 'center16777215', text = n[3]))
			elif n[1] != '1' and n[2] != '16777215':
				self.danmu_list.append(static_events.format(start_time = time_tup[0], end_time = time_tup[1],style = 'center'+n[2], text = n[3]))
		print '\033[1;36m弹幕装填完毕 \033[1;32m【 OK 】\033[0m'
		


	def write_file(self, filename):
		with open(filename+'.ssa','w') as f:
			f.writelines(self.item[0]+'\n')
			for m, n in self.script_info.iteritems():
				info = m+': '+n+'\n'
				f.writelines(info)
			f.writelines(self.item[1]+'\n')
			f.writelines('Format'+self.v4_styles.get('Format')+'\n')
			for p,q in self.style.iteritems():
				content  = 'Style: '+q+'\n'
				f.writelines(content)
			f.writelines(self.item[2]+'\n')
			for i in self.danmu_list:
				f.writelines(i+'\n')
		print '\033[1;36m弹幕装填类型 \033[1;32m【普通】\033[0m'


def deal_filename(filename):
	return re.escape(filename)




def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "f:l:hu", ["file=", "link=", "help", "update"])
	except getopt.GetoptError, e:
		print " \033[0;31mError 请尝试执行'--help'来获取更多信息 \033[0m"
		sys.exit(2)
	fan = Danmu()
	for opt, arg in opts:
		if opt in ("-f","--file"):
			files = arg
			filename = files.split('.')[0]
		elif opt in ('-l',"--link"):
			fan.get_danmu(arg)
			fan.deal_danmu()
			fan.write_file(filename)
		elif opt in ("-h", "--help"):
			print 'this is helpdoc'
		elif opt in ("-u", "--update"):
			print 'the data is updating'
	if config.ENALLE_OPEN == 'on':
		command = 'xdg-open ' + deal_filename(files)
		os.system(command)

			
if __name__ == '__main__':
	main()
