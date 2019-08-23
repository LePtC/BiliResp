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

    try:
        print(msg) # TODO 这里有概率出 'gbk' codec 错误，但jupyter测试又不能复现
    except Exception as e:
        print(e)

    try:
        print(uri)
    except Exception as e:
        print(e)

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
                        }
                        )
    try:
        print(resp.text)
    except Exception as e:
        print(e)


summary_list = '卖萌、复读、讲笑话、念诗…'

import random
def ran_face():
  return random.choice(['(⌒▽⌒)', '(｀・ω・´)', '(◦˙▽˙◦)', '(=・ω・=)', '_Σ:з」∠)シ', 'o(∩_∩)o', '(〜￣▽￣)〜','>_<', '(๑• ▽ •๑)'])
def ran_han():
  return random.choice(['(;¬_¬)', '(~_~;)', ' = =!', '╮(╯▽╰)╭', '(シ_ _)シ', '>_<', '(๑• _ •๑)', '(:3_ヽ)_'])


with open(path2+'jokes.txt', 'r', encoding='utf-8') as file:
    joke_list = [x.replace("\n","") for x in file.readlines()]

with open(path2+'lyrics.txt', 'r', encoding='utf-8') as file:
    lyric_list = [x.replace("\n","") for x in file.readlines()]

with open(path2+'popus.txt', 'r', encoding='utf-8') as file:
    popu_list = [x.replace("\n","") for x in file.readlines()]

with open(path2+'poems.txt', 'r', encoding='utf-8') as file:
    poem_list = [x.replace("\n","") for x in file.readlines()]

# 神器，能从语料库找最接近字符串
import difflib

def zhineng_reply(atstr,atmid,oid,parent,root,uri,bid):

    atstr = atstr.replace('@狸工智能 ', '', 1).replace('@狸工智能', '', 1)
    atstr_clean = atstr.strip('？！，。；“”‘’@?!,.;"…一个啊吧的是了我你他们说不在有这个上来到时为什么啥人')

    if len(re.findall(r'用法|指南|说明|帮助|关键词|(怎么|可以)(问|查)|你(.{0,2})家|help',atstr)) > 0:
        po_txt = '问我的详细指南见：http://github.com/LePtC/BiliResp '+ran_face()

    elif len(re.findall(r'（有损复读',atstr)) > 0: # 糖指令
        po_txt = atstr.replace('（有损复读', '', 1)

    elif len(re.findall(r'复读|人类(.{0,2})本质|快乐',atstr)) > 0:
        po_txt = atstr

    if len(re.findall(r'你(.{0,4})回|回复|回(.{0,1})我',atstr)) > 0:
        po_txt = '目前每5分钟看一次艾特，每次最多回20条，如果回复太多遇到验证码我就回不了啦 '+ran_han()

    if len(re.findall(r'在(.{0,1})(吗|？|?)',atstr)) > 0:
        po_txt = random.choice(['我在鸭 '+ran_face(),atstr])

    if len(re.findall(r'你好|哈喽|hello',atstr)) > 0:
        po_txt = random.choice(['你也好鸭 ',atstr.replace('你好', '你也好', 1),atstr])+ran_face()

    elif len(re.findall(r'(n|牛|流)(b|B|比|逼|弊|蔽|啤)',atstr)) > 0:
        po_txt = random.choice(['狸子nb！','狸子nb！（破音'])+ran_face()

    elif len(re.findall(r'狸(.{0,3})叫|fox(.{0,3})say|喵|嘤',atstr)) > 0:
        po_txt = random.choice(['嘤','嘤嘤嘤','嘤嘤嘤嘤嘤','大楚兴，陈胜王'])+ran_face()

    elif len(re.findall(r'(卖|买)(.{0,3})萌',atstr)) > 0:
        po_txt = '狸子'+random.choice(['敲','敲极'])+random.choice(['可','阔'])+'爱～'+ran_face()

    elif len(re.findall(r'么么|摸(.{0,4})(狐|狸|您|你)|(可|喜)爱|喜(欢|感)|萌|高兴|(快|欢)乐|愉快|幸福|好玩|笑死|xswl',atstr)) > 0:
        po_txt = random.choice(['狐狸搓一搓，生活欢乐多～','狐狸揉一揉，生活不发愁～','狐狸摸一摸，生活欢乐多～'])+ran_face()

    elif len(re.findall(r'你(喜欢|爱)',atstr)) > 0: # TODO 确定主人公后再细分
        po_txt = random.choice(['我最喜欢狸子啦','小孩子才做选择','我全都要.jpg'])+ran_face()

    elif len(re.findall(r'你是|真人|自(.{0,3})介绍|介绍(.{0,4})自|你(.{0,3})(爸|妈|父|母)',atstr)) > 0: # 把你是谁放宽到你是了…
        po_txt = '我是狸子LePtC研发'+random.choice(['','时长两天半'])+'的虚拟UP主'+random.choice(['～','鸭'])+ran_face()

    elif len(re.findall(r'(?i)(LePtC|萌狸|狸(子|君|酱|神))(.{0,4})(生日|几岁|多大|出生|破壳)|修仙|成精',atstr)) > 0:
        po_txt = '狸子是公元199东汉末年出生的狐狸（生日连它自己都不记得辣），建国前成的精～'+ran_face()

    elif len(re.findall(r'(你|狸工智能)(.{0,4})(男|女)',atstr)) > 0:
        po_txt = '我是AI，没有性别'+random.choice(['的奥','哒'])+ran_face()

    elif len(re.findall(r'(你|狸工智能)(.{0,4})(生日|几岁|多大|出生|破壳)',atstr)) > 0:
        po_txt = '我是从2019年8月16号开始试运行'+random.choice(['的奥','哒'])+ran_face()

    elif len(re.findall(r'(?i)(LePtC|萌狸|狸(子|君|酱|神))(.{0,4})男|你(.{0,4})女',atstr)) > 0:
        po_txt = '狸子是男狐狸'+random.choice(['奥，','～'])+'其它保密 '+ran_face()

    elif len(re.findall(r'你会',atstr)) > 0:
        po_txt = random.choice(['','我'])+'现在会的有'+summary_list+ran_han()

    elif len(re.findall(r'唱(.{0,4})歌',atstr)) > 0:
        close_txt = difflib.get_close_matches(atstr_clean.strip('唱歌'), lyric_list, 9, 0.01)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)+ran_face()
        else:
            po_txt = random.choice(lyric_list)+ran_face()

    elif len(re.findall(r'笑话|段子|聊|唠嗑|(智|制|滞)(.{0,2})(障|杖|帐|涨)|笨蛋|你(.{0,4})抽|沙雕|傻|骚话',atstr)) > 0:
        close_jokes = difflib.get_close_matches(atstr_clean.strip('讲笑话段子聊唠嗑智制滞障杖帐涨笨蛋抽沙雕傻'), joke_list, 9, 0.01)
        if len(close_jokes) > 0:
            po_txt = random.choice(close_jokes)
        else:
            po_txt = random.choice(joke_list)

    elif len(re.findall(r'睡觉|晚安|失眠',atstr)) > 0: # TODO 睡了吗
        po_txt = random.choice(['晚安啦～祝你睡个好觉','天上的星星不说话，地上的娃娃想妈妈','夜莺代我向你道晚安'])+ran_face()

    elif len(re.findall(r'怕',atstr)) > 0:
        po_txt = '我最怕断电、断网、欠费停机…'+ran_han()

    elif len(re.findall(r'报废',atstr)) > 0:
        po_txt = random.choice(['我真的还想再活五百年——','我属于什么垃圾？','没有治疗价值了吗？','我没有中暑也没有抑郁，每天吃的不多也不少，我不漂亮也不丑，没有淋雨也不打架…'])+ran_han()

    elif len(re.findall(r'博士',atstr)) > 0:
        po_txt = random.choice(['一人去算命，算命先生摸骨相面掐算八字后，说：“你二十岁恋爱，二十五岁结婚，三十岁生子，一生富贵平安家庭幸福晚年无忧。”此人先惊后怒，道：“我今年三十五，博士，光棍，木有恋爱。”先生闻言，略微沉思后说：“年轻人，知识改变命运啊！”','本科、硕士、博士生要写“如何做红烧肉”。本科生说把肉放到锅里加些东西煮，一个月后交稿。硕士生说这个是不行的，要写出多少肉，多少其他的佐料，怎么煮，煮多长时间，半年后才写完。又过了两三年，博士生出了厚厚的一本《如何做红烧肉》，打开目录：“第一章，如何养猪”。','一个清华博士生、一个本科生、一个附中学生约定要在周一见一面，本科生迟到了：“抱歉，我周末晚上赶个DDL赶到凌晨2点。”“什么是DDL？”附中学生问。“什么是周末？”博士生问。'])+ran_han()

    elif len(re.findall(r'清华|THU|T大|五道口',atstr)) > 0:
        po_txt = random.choice(['西山苍苍，东海茫茫，吾校庄严，四个操场','天行健，君子以自强不息','清华百年校庆当天，学校西门挤满了想混进去的游客。一位游客看了看，在门外拍了几张相片就走了，旁边的游客问他：“就拍这个？”那人说：“本来想拍校庆的，现在也还不错，拍了个西门庆。”'])+ran_face()

    elif len(re.findall(r'北大|北京大学',atstr)) > 0:
        po_txt = random.choice(['北大还行撒贝宁','狸子：北大nb！'])+ran_face()

    elif len(re.findall(r'女装',atstr)) > 0:
        po_txt = random.choice(['女装只有零次和无数次','我不能露脸的，我要过十万订阅才能露','程序员穿女装能大大提升敲击速度，而且还能减少BUG的发生','自学JAVA太苦了，不如…试试女装？','三流码农写UI，二流码农写架构，一流码农写算法，顶级码农穿女装','给大佬递女装.jpg'])+ran_face()

    elif len(re.findall(r'dark|♂',atstr)) > 0:
        po_txt = random.choice(['deep♂dark♂fantasy','啊 乖乖站好','I♂like♂van♂游戏',"you are so dark, you sure you're not from DC?"])+ran_face()

    elif len(re.findall(r'蔡|(徐|虚)坤|cxk',atstr)) > 0:
        close_txt = difflib.get_close_matches(atstr_clean.strip('蔡徐坤cxk'), popu_list, 5, 0.07)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)+ran_face()
        else:
            po_txt = random.choice(['喜欢唱，跳，rap，律师函','吾与城北徐坤孰美？','狸子喜欢去沙滩，因为基尼太美 ','庄颜坐在罗辑边上，眼里冒着小星星。罗辑笑着问：你一直看着我干嘛？庄颜花痴地说道：辑你太美','一千年后，人类社会高度发达，但是煤的存量也一天天减少，科学家为了解决这一困境，运用拟态理论成功复制出了代替品，即拟态煤'])+ran_face()

    elif len(re.findall(r'乔碧|碧萝|坦克|乔奶|按(f|F)',atstr)) > 0:
        close_txt = difflib.get_close_matches(atstr_clean.strip('乔碧萝坦克'), popu_list, 5, 0.07)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)+ran_face()
        else:
            po_txt = random.choice(['我不能露脸的，我要过十万订阅才能露','按F键进入坦克','榜一连夜扛着火车跑了'])+ran_face()

    elif len(re.findall(r'卢本伟|lbw',atstr)) > 0:
        close_txt = difflib.get_close_matches(atstr_clean.strip('卢本伟lbw'), popu_list, 5, 0.07)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)+ran_face()
        else:
            po_txt = random.choice(['没有开挂lbw','我怀疑你消费过世主播并且证据确凿','lbwnb!','你能秒我，我就当场把这个电脑屏幕吃掉'])+ran_face()

    elif len(re.findall(r'对象',atstr)) > 0:
        po_txt = '狸子教你新建一个对象 av29577482'+ran_face()

    elif len(re.findall(r'漂亮',atstr)) > 0:
        po_txt = random.choice(['漂亮警告（露出悲伤的笑容 ','小汽车呀！真漂亮，嘟嘟嘟嘟嘟嘟嘟喇叭响。'])+ran_face()

    elif len(re.findall(r'帅',atstr)) > 0:
        po_txt = '冲在前线的'+random.choice(['消防员','警察叔叔','兵哥哥'])+'最帅啦'+ran_face()

    elif len(re.findall(r'来',atstr)) > 0:
        po_txt = random.choice(['来了来了，咕','来啊，复相伤害啊','来啊，快活啊'],atstr)+ran_han()

    elif len(re.findall(r'em',atstr)) > 0:
        po_txt = random.choice(['emmmmm','恶魔麻麻买面膜mmm'],atstr)

    # 全失败后，开始交给difflib寻找最接近（智障）回复
    else:
        close_txt = difflib.get_close_matches(atstr_clean, lyric_list, 5, 0.1)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)
        else:
            close_txt = difflib.get_close_matches(atstr_clean, popu_list, 5, 0.07)
            if len(close_txt) > 0:
                po_txt = random.choice(close_txt)
            else:
                close_txt = difflib.get_close_matches(atstr_clean, poem_list, 5, 0.05)
                if len(close_txt) > 0:
                    po_txt = random.choice(close_txt)
                else:
                    po_txt = '（这条艾特中没有可回复的关键词'+random.choice(['～','诶'])+ran_han()

    po_reply(po_txt,oid,parent,root,uri,bid)


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
last_id = int(os.popen('more '+path2+'last_id.txt').read().replace("\n",""))
new_id = last_id # 新回复的时间戳中取最大者

for atli in tmp['data']['items']:
    this_id = int(atli['at_time'])
    if this_id > last_id :
        if this_id >= new_id:
            new_id = this_id
            print('new:',new_id)
            os.system('echo '+str(new_id)+' > '+path2+'last_id.txt')
        try:
            print(atli['item']['source_content'])
            zhineng_reply(atli['item']['source_content'],atli['user']['mid'],atli['item']['subject_id'],atli['item']['source_id'],atli['item']['target_id'],atli['item']['uri'],atli['item']['business_id'])
        except Exception as e:
            print(e)



# file = open(path2+'last_id.txt', 'w')
# file.write(str(new_id))
# file.close()

