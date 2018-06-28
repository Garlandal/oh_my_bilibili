# coding: utf-8

from __future__ import division
from collections import Counter

import argparse
import platform
import json
import sys
import re
import requests
import config
import copy
import os


def prettify_print(type_, text, status_text=''):
    color_dict = {
        'ok': '\033[1;32m',
        'info': '\033[1;36m',
        'error': '\033[0;31m',
        'end': '\033[0m'
    }
    s = '%s%s{}%s' % (color_dict[type_], text, color_dict['end'])
    inner_s = ' {}【{}】'.format(color_dict['ok'], status_text) if status_text else ''
    print(s.format(inner_s))


class Danmu():
    """Download Danmaku and save as ssa file"""

    def __init__(self):
        self.comment_url = 'http://comment.bilibili.com/'
        self.script_info = config.SCRIPT_INFO
        self.v4_styles = config.V4_STYLES
        self.events = config.EVENTS
        self.item = ('[Script Info]', '[v4 Styles] ', '[Events]')
        self.session = requests.Session()
        self.danmu_dict = {}
        self.style = {}
        self.danmu_list = []

    def _xml_url(self, cid):
        return ''.join([self.comment_url, str(cid), '.xml'])

    def _parse_xml(self, xml):
        pat = re.compile(r'<d p="(.*?)">(.*?)</d>')
        for full_content, text in re.findall(pat, xml):
            ctime, type_, _, color, _, _, _, pool = full_content.split(',')
            self.danmu_dict[pool] = [ctime, type_, color, text]

    def time_format(self, time, types):
        time = float(time)
        if types == '1':
            endtime = time + 11
        else:
            endtime = time + 4
        start = str(int(time / 3600)) + ':' + str(int(time / 60)) + ':' + str(int(time % 60)) + '.' + str(
            time % 60 - int(time % 60))[2:4]
        end = str(int(endtime / 3600)) + ':' + str(int(endtime / 60)) + ':' + str(int(endtime % 60)) + '.' + str(
            endtime % 60 - int(endtime % 60))[2:4]
        return (start, end)

    def get_danmu(self, url):
        prettify_print('info', '喵娘正在启动', 'OK')
        content = self.session.get(url).content
        prettify_print('info', '解析視頻地址', 'OK')
        if len(content) < 10000:
            prettify_print('error', "Error 解析失败")
            sys.exit(2)

        pat = re.compile(r'"epInfo":(.*?),"epList')
        ep_info = re.findall(pat, content)[0]
        xml_url = self._xml_url(json.loads(ep_info)['cid'])
        comment_xml = self.session.get(xml_url).content
        self._parse_xml(comment_xml)

        danmaku_counter = Counter([len(p[3]) for q, p in self.danmu_dict.iteritems()])
        self.danmu_counts = sorted(danmaku_counter.most_common(200))
        prettify_print('info', '全舰弹幕装填', '......')

    def deal_danmu(self):
        white_style, color_style, center_style, centerw_style = self.v4_styles.get('Style')
        rolling_events = self.events.get('rolling')
        static_events = self.events.get('static')
        deal_dict = copy.deepcopy(self.danmu_dict)
        count_list = [i[0] for i in self.danmu_counts]
        del_list = [single_id for single_id, content in deal_dict.iteritems() if len(content[3]) not in count_list]
        map(lambda x: deal_dict.pop(x), del_list)
        for m, n in deal_dict.iteritems():
            time_tup = self.time_format(n[0], n[1])
            if n[2] != '16777215' and n[1] == '1':
                self.style[n[2]] = color_style.format(style=n[2], color_code=n[2])
            elif n[2] == '16777215' and n[1] == '1':
                self.style['16777215'] = white_style.format(style='16777215')
            elif n[2] == '16777215' and n[1] != '1':
                self.style['center16777215'] = centerw_style.format(style='center16777215')
            elif n[2] != '16777215' and n[1] != '1':
                self.style['center' + n[2]] = center_style.format(style='center' + n[2], color_code=n[2])
            if n[1] == '1' and n[2] == '16777215':
                self.danmu_list.append(
                    rolling_events.format(start_time=time_tup[0], end_time=time_tup[1], style='16777215', text=n[3]))
            elif n[1] == '1' and n[2] != '16777215':
                self.danmu_list.append(
                    rolling_events.format(start_time=time_tup[0], end_time=time_tup[1], style=n[2], text=n[3]))
            elif n[1] != '1' and n[2] == '16777215':
                self.danmu_list.append(
                    static_events.format(start_time=time_tup[0], end_time=time_tup[1], style='center16777215',
                                         text=n[3]))
            elif n[1] != '1' and n[2] != '16777215':
                self.danmu_list.append(
                    static_events.format(start_time=time_tup[0], end_time=time_tup[1], style='center' + n[2],
                                         text=n[3]))
        prettify_print('info', '弹幕装填完毕', 'OK')

    def write_file(self, filename):
        with open(filename + '.ssa', 'w') as f:
            f.writelines(self.item[0] + '\n')
            for m, n in self.script_info.iteritems():
                info = m + ': ' + n + '\n'
                f.writelines(info)
            f.writelines(self.item[1] + '\n')
            f.writelines('Format' + self.v4_styles.get('Format') + '\n')
            for p, q in self.style.iteritems():
                content = 'Style: ' + q + '\n'
                f.writelines(content)
            f.writelines(self.item[2] + '\n')
            for i in self.danmu_list:
                f.writelines(i + '\n')
        prettify_print('info', '弹幕装填类型', '普通')


def main(args):
    filename = args.file
    url = args.link
    if not filename or not url:
        prettify_print('error', "Error 请尝试执行'--help'来获取更多信息")
        sys.exit(2)

    fan = Danmu()
    fan.get_danmu(url)
    fan.deal_danmu()
    fan.write_file(filename)

    if config.ENALLE_OPEN == 'on':
        open_command = {
            'Linux': 'xdg-open',
            'Darwin': 'open'
        }[platform.system()]
        command = ' '.join([open_command, re.escape(filename)])
        os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='local video file')
    parser.add_argument('link', help='bilibili video page link')
    args = parser.parse_args()
    main(args)
