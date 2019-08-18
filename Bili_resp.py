import requests
import re
import sys


import getpass
path = 'C:\\Users\\'+getpass.getuser()+'\\Downloads\\BiliServ\\' #这里用你自己的帐号cookie测试
f_cookie = open(path+'cookie.txt', 'r', encoding='UTF-8')
cookie = f_cookie.read()
csrf = re.findall(r'bili_jct=([^;]+);',cookie)[0]

bilibili_headers = {a:b for a,b in re.findall(r'([^:\n]+): (.+)', '''
Host: api.bilibili.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://message.bilibili.com/
Origin: https://message.bilibili.com
Connection: keep-alive
''')}
bilibili_headers.update( {'Cookie' : cookie} )

import json
tmp = json.loads(requests.get("https://api.bilibili.com/x/msgfeed/at", headers = bilibili_headers).text)

# 一次获取最新20个艾特消息，提取有用的存入dict
# len(tmp['data']['items'])
atli = tmp['data']['items'][0]
atstr = atli['item']['source_content']
atmid = atli['user']['mid']
oid = atli['item']['subject_id']
parent = atli['item']['source_id']
root = atli['item']['target_id']


def po_reply(msg,oid,parent,root):
    resp = requests.post('https://api.bilibili.com/x/v2/reply/add',
                  headers={'Host':'api.bilibili.com',
                           'Cookie': cookie,
                           'Refer': "https://t.bilibili.com"},
                  data = {"csrf": csrf,
                        "oid": oid,
                        "type": "11",
                        "root": root,
                        "parent": parent,
                        "message": msg,
                        "plat": "1",
                        "jsonp": "jsonp"
})
    print(resp.text)


import random
def ran_face():
  return random.choice(['(⌒▽⌒)', '(｀・ω・´)', '(◦˙▽˙◦)', '(=・ω・=)', '_Σ:з」∠)シ', 'o(∩_∩)o', '(〜￣▽￣)〜'])

if len(re.findall(r'怎么(问|查)|用法|指南|说明|帮助|你(.{0,2})家|help|F1|f1',atstr)) > 0:
    po_reply('狸工智能的用法：http://github.com/LePtC/BiliResp '+ran_face(),oid,parent,root)
    sys.exit()

if len(re.findall(r'狸(.{0,3})叫|fox(.{0,3})say',atstr)) > 0:
    po_reply(random.choice(['嘤','嘤嘤嘤','嘤嘤嘤嘤嘤','大楚兴，陈胜王'])+ran_face(),oid,parent,root)
    sys.exit()

if len(re.findall(r'卖(.{0,3})萌',atstr)) > 0:
    po_reply('狸子'+random.choice(['敲','敲极'])+random.choice(['可','阔'])+'爱～'+ran_face(),oid,parent,root)
    sys.exit()


# if re.findall(r'查(.+)排名',atstr)[0] == '我'
