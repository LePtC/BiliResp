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


# 一次获取最新20个艾特消息
import json
tmp = json.loads(requests.get("https://api.bilibili.com/x/msgfeed/at", headers = bilibili_headers).text)

bilibili_headers2 = {a:b for a,b in re.findall(r'([^:\n]+): (.+)', '''
Host: api.bilibili.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0 Waterfox/56.2.12
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 224
DNT: 1
Connection: keep-alive
Content-Length: 234
''')}
bilibili_headers2.update( {'Cookie' : cookie} )

from urllib.parse import urlparse

def po_reply(msg,oid,parent,root,uri,bid):
    print(uri)
    bilibili_headers2.update( {'Referer' : uri} )
    bilibili_headers2.update( {'Origin' : 'https://'+urlparse(uri).hostname} )
    resp = requests.post('https://api.bilibili.com/x/v2/reply/add',
                  headers=bilibili_headers2,
                  data = {"csrf": csrf,
                        "oid": oid,
                        "type": bid, #专栏是www.12，动态t.17，相册h.11
                        "root": root,
                        "parent": parent,
                        "message": msg,
                        "plat": "1",
                        "jsonp": "jsonp"
})
    print(resp.text)


summary_list = '用法、卖萌、狸叫'

import random
def ran_face():
  return random.choice(['(⌒▽⌒)', '(｀・ω・´)', '(◦˙▽˙◦)', '(=・ω・=)', '_Σ:з」∠)シ', 'o(∩_∩)o', '(〜￣▽￣)〜','>_<'])
def ran_han():
  return random.choice(['(;¬_¬)', '(~_~;)', ' = =!', '╮(╯▽╰)╭', '(シ_ _)シ','>_<'])

def zhineng_reply(atstr,atmid,oid,parent,root,uri,bid):

    if len(re.findall(r'用法|指南|说明|帮助|(怎么|可以)(问|查)|你(.{0,2})家|help',atstr)) > 0:
        po_reply('目前支持的关键词有：'+summary_list+'……详细指南见：http://github.com/LePtC/BiliResp '+ran_face(),oid,parent,root,uri,bid)
        return 0

    if len(re.findall(r'狸(.{0,3})叫|fox(.{0,3})say',atstr)) > 0:
        po_reply(random.choice(['嘤','嘤嘤嘤','嘤嘤嘤嘤嘤','大楚兴，陈胜王'])+ran_face(),oid,parent,root,uri,bid)
        return 0

    if len(re.findall(r'卖(.{0,3})萌',atstr)) > 0:
        po_reply('狸子'+random.choice(['敲','敲极'])+random.choice(['可','阔'])+'爱～'+ran_face(),oid,parent,root,uri,bid)
        return 0

    if len(re.findall(r'你是',atstr)) > 0:
        po_reply('我是狸子LePtC研发'+random.choice(['','时长两天半'])+'的虚拟UP主'+random.choice(['～','鸭'])+ran_face(),oid,parent,root,uri,bid)
        return 0

    if len(re.findall(r'你会',atstr)) > 0:
        po_reply(random.choice(['','我'])+'现在只会卖萌'+ran_han(),oid,parent,root,uri,bid)
        return 0


# if re.findall(r'查(.+)排名',atstr)[0] == '我'







# len(tmp['data']['items'])
# atli = tmp['data']['items'][0]
# atstr = atli['item']['source_content']
# atmid = atli['user']['mid']
# oid = atli['item']['subject_id']
# parent = atli['item']['source_id']
# root = atli['item']['target_id']

import os
path2 = 'C:\\Users\\'+getpass.getuser()+'\\Downloads\\BiliResp\\'

# 读取上次回复过的最后一个消息时间戳（避免重复回复，试过用id结果居然不单增…）
last_id = int(os.popen('more '+path2+'last_id.txt').read().replace ("\n",""))
new_id = last_id # 新回复的时间戳中取最大者

for atli in tmp['data']['items']:
    this_id = int(atli['at_time'])
    if this_id > last_id :
        if this_id >= new_id:
            new_id = this_id
            print('new:',new_id)
            os.system('echo '+str(new_id)+' > '+path2+'last_id.txt')
        try:
            zhineng_reply(atli['item']['source_content'],atli['user']['mid'],atli['item']['subject_id'],atli['item']['source_id'],atli['item']['target_id'],atli['item']['uri'],atli['item']['business_id'])
        except Exception as e:
            print(e)



# file = open(path2+'last_id.txt', 'w')
# file.write(str(new_id))
# file.close()

