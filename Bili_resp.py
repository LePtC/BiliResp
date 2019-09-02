#coding:utf-8
import requests
import re
import sys
import os


import getpass
path = 'C:\\Users\\'+getpass.getuser()+'\\Downloads\\BiliServ\\' #这里用你自己的帐号cookie测试
path2 = 'C:\\Users\\'+getpass.getuser()+'\\Downloads\\BiliResp\\'

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


summary_list = '卖萌、复读、讲笑话、念诗…'

import random

with open(path2+'ran_faces.txt', 'r', encoding='utf-8') as file:
    ran_face_list = [x.replace("\n","") for x in file.readlines()]
with open(path2+'ran_hans.txt', 'r', encoding='utf-8') as file:
    ran_han_list = [x.replace("\n","") for x in file.readlines()]
def ran_face():
  return random.choice(ran_face_list)
def ran_han():
  return random.choice(ran_han_list)


with open(path2+'jokes.txt', 'r', encoding='utf-8') as file:
    joke_list = [x.replace("\n","") for x in file.readlines()]
with open(path2+'phds.txt', 'r', encoding='utf-8') as file:
    phd_list = [x.replace("\n","") for x in file.readlines()]

with open(path2+'lyrics.txt', 'r', encoding='utf-8') as file:
    lyric_list = [x.replace("\n","") for x in file.readlines()]

with open(path2+'popus.txt', 'r', encoding='utf-8') as file:
    popu_list = [x.replace("\n","") for x in file.readlines()]

with open(path2+'poems.txt', 'r', encoding='utf-8') as file:
    poem_list = [x.replace("\n","") for x in file.readlines()]

with open(path2+'peoples.txt', 'r', encoding='utf-8') as file:
    people_list = [x.replace("\n","") for x in file.readlines()]


def stripall(st,chs):
    str_clean = st
    for ch in list(chs):
        str_clean = str_clean.replace(ch,'')
    return str_clean


# 神器，能从语料库找最接近字符串
import difflib

def zhineng_reply(atstr,atmid,oid,parent,root,uri,bid):

    # 不友好不回（后期注意避开UP名字
    if len(re.findall(r'(?i)给爷|wcn|cnm|nm(b|d|s)|尼玛|艹|骂|弟弟|dd|kkp|废青',atstr)) > 0:
        print('检测到不友好')
        po_txt = ''
        return 0

    atstr = atstr.replace('@狸工智能 ', '').replace('@狸工智能', '')
    # 忽略中括号表情
    temp_face = re.findall(r'\[(.{1,10})\]',atstr)
    if len(temp_face) > 0:
        atstr = atstr.replace('['+temp_face[0]+']', '')
    atstr_clean = stripall(atstr,'？！，。；“”‘’（）～@?!,.;"()…~一个啊吧啦的是了我你他们说不在有这个上下来到时为什么怎样啥呢人和如果何要接')


    if len(re.findall(r'用法|指南|说明|帮助|功能|关键词|(怎么|可以)(问|查)|help',atstr)) > 0:
        po_txt = '问我的详细指南见：http://github.com/LePtC/BiliResp '+ran_face()

    elif len(re.findall(r'（精准复读',atstr)) > 0: # 糖指令，TODO 艾特自己会死循环？
        po_txt = atstr.replace('（精准复读', '', 1)

    elif len(re.findall(r'复读|人类(.{0,2})本质|快乐',atstr)) > 0:
        po_txt = atstr.replace('我', '你')

    elif len(re.findall(r'你(.{0,4})回|回复|回(.{0,1})我',atstr)) > 0:
        po_txt = '目前每5分钟看一次艾特（B站任意评论区艾特均可），每次最多回20条，如果消息太多遇到验证码我就回不了啦 '+ran_han()

    elif len(re.findall(r'博士',atstr)) > 0:
        po_txt = random.choice(phd_list)+ran_han()

    elif len(re.findall(r'清华|THU|T大|五道口',atstr)) > 0:
        if len(re.findall(r'如何|怎(么|样)|教我',atstr)) > 0:
            po_txt = '乘北京地铁，在五道口站A口出可达清华东南门，在圆明园站C口出可达清华西校门'
        else:
            po_txt = random.choice(['西山苍苍，东海茫茫，吾校庄严，四个操场','天行健，君子以自强不息','个个都是人才，说话又好听，唔呦，超喜欢在里面的','清华百年校庆当天，学校西门挤满了想混进去的游客。一位游客看了看，在门外拍了几张相片就走了，旁边的游客问他：“就拍这个？”那人说：“本来想拍校庆的，现在也还不错，拍了个西门庆。”'])

    elif len(re.findall(r'北大|北京大学',atstr)) > 0:
        po_txt = random.choice(['北大还行撒贝宁','狸子：北大nb！'])+ran_face()

    elif len(re.findall(r'女装',atstr)) > 0:
        po_txt = random.choice(['女装只有零次和无数次','程序员穿女装能大大提升编程速度，而且还能减少BUG的发生','自学JAVA太苦了，不如…试试女装？','三流码农写UI，二流码农写架构，一流码农写算法，顶级码农穿女装','给大佬递女装.jpg'])+ran_face()

    # 捕获LePtC主语
    elif len(re.findall(r'(?i)(LePtC|(萌|啊|阿)狸|狸(子|君|酱|神))|你(.{0,2})(up|UP|爸|妈|主)',atstr)) > 0:
        if len(re.findall(r'是(谁|？|\?)',atstr)) > 0:
            po_txt = '敲可爱的狸子LePtC，是个宝藏UP主' + ran_face()
        elif len(re.findall(r'(啥|什么)时',atstr)) > 0:
            po_txt = '狸子是B站认证过的佛系UP主，一切随缘～' + ran_face()
        elif len(re.findall(r'喜欢说',atstr)) > 0:
            po_txt = random.choice(['嘤嘤嘤','狸子敲'+random.choice(['可','阔'])+'爱～','狐狸搓一搓，生活欢乐多～']) + ran_face()
        elif len(re.findall(r'掉粉',atstr)) > 0:
            po_txt = random.choice(['嘤嘤嘤','我觉得布星']) + ran_han()
        elif len(re.findall(r'(?i)榜|nb|第一',atstr)) > 0:
            po_txt = random.choice(['嘤嘤嘤','狸子冲鸭～','狸子加油！']) + ran_face()
        elif len(re.findall(r'你(.{0,2})(喜欢|稀饭)',atstr)) > 0:
            po_txt = random.choice(['人人都喜欢狸子啦','狸子'+random.choice(['敲','敲极'])+random.choice(['可','阔'])+'爱～','狸子敲可爱，想…'])
        elif len(re.findall(r'帅',atstr)) > 0:
            po_txt = random.choice(['狸子带帅比（','帅有什么用？还不是会被卒吃掉','狸子修八尺有余，而形貌昳丽'])
        elif len(re.findall(r'觉得|谁更|爱|萌',atstr)) > 0:
            po_txt = random.choice(['狸子nb！','狸子nb！（破音','狸子冲鸭～','狸子'+random.choice(['敲','敲极'])+random.choice(['可','阔'])+'爱～','狸子敲可爱，想…','告诉狸子我还爱♂他'])
        elif len(re.findall(r'生日|岁|多大|出生|破壳|修仙|成精|介绍',atstr)) > 0:
            po_txt = '狸子是公元199年出生的狐狸，建国前成的精～'
        elif len(re.findall(r'男|女|单身|婚',atstr)) > 0:
            po_txt = '我只知道狸子是只男狐狸' + ran_face()
        elif len(re.findall(r'学',atstr)) > 0:
            po_txt = '某职业技术学校，地球Online源码逆向工程专业'
        elif len(re.findall(r'关系|你(.{0,2})叫',atstr)) > 0:
            po_txt = '狸子是我的首席铲屎官呢' + ran_face()
        elif len(re.findall(r'晚|修',atstr)) > 0:
            po_txt = '狸子每天晚上都要修♂理我' + ran_han()
        else:
            close_txt = difflib.get_close_matches(stripall(atstr_clean,'LePtC'), popu_list+poem_list, 5, 0.1)
            if len(close_txt) > 0:
                po_txt = random.choice(close_txt)
            else:
                po_txt = '你想问狸子什么？' + ran_face()


    elif len(re.findall(r'你是|真人|自(.{0,3})介绍|介绍(.{0,4})自|你(.{0,3})(爸|妈|父|母|主)(.{0,3})(是|谁)',atstr)) > 0: # 把你是谁放宽到你是了…
        po_txt = '我是狸子LePtC研发'+random.choice(['','时长两天半'])+'的虚拟UP主'+random.choice(['～','鸭'])+ran_face()

    elif len(re.findall(r'狸(.{0,3})叫|fox(.{0,3})say|嘤',atstr)) > 0:
        po_txt = random.choice(['嘤','嘤嘤嘤','嘤嘤嘤嘤嘤','大楚兴，陈胜王'])+ran_face()

    elif len(re.findall(r'(卖|买)(.{0,3})萌',atstr)) > 0:
        po_txt = '狸子'+random.choice(['敲','敲极'])+random.choice(['可','阔'])+'爱～'+ran_face()

    elif len(re.findall(r'笑话|段子|聊|唠嗑|(智|制|滞)(.{0,2})(障|杖|帐|涨)|笨蛋|你(.{0,4})抽|沙雕|傻|骚话',atstr)) > 0:

        close_jokes = difflib.get_close_matches(stripall(atstr_clean,'讲个笑话段子聊唠嗑狸工智制滞障杖帐涨笨蛋抽沙雕傻骚话'), joke_list, 9, 0.01)
        if len(close_jokes) > 0:
            po_txt = random.choice(close_jokes)
        else:
            po_txt = random.choice(joke_list)

    elif len(re.findall(r'睡(觉|啦)|晚安|失眠|这么晚|凌晨',atstr)) > 0: # TODO 睡了吗
        po_txt = random.choice(['晚安啦～祝你睡个好觉','天上的星星不说话，地上的娃娃想妈妈 zzZ','夜莺代我向你道晚安','快快睡个好觉 '])+ran_face()

    elif len(re.findall(r'(报|收)废|垃圾',atstr)) > 0:
        po_txt = random.choice(['我真的还想再活五百年——','我属于什么垃圾？','没有治疗价值了，拉到河边烤了吧','我没有中暑也没有抑郁，每天吃的不多也不少，我不漂亮也不丑，没有淋雨也不打架…'])+ran_han()

    elif len(re.findall(r'(?i)dark|♂|约(吗|不)|屁股|van|哲学',atstr)) > 0:
        po_txt = random.choice(['deep♂dark♂fantasy','啊 乖乖站好','I♂like♂van♂游戏','来我家玩吧，我家还蛮大♂的','让我康康（震声'])+ran_face()

    elif len(re.findall(r'真香|境泽',atstr)) > 0:
        po_txt = random.choice(['当初就不该吃那碗饭.jpg','铁骨铮铮王境泽','我就是饿死…真香','来一口老弟～'])+ran_face()

    elif len(re.findall(r'思聪',atstr)) > 0:
        po_txt = random.choice(['当初就不该吃那个热狗.jpg','王司徒！（战争践踏.jpg'])+ran_face()

    elif len(re.findall(r'蔡|(徐|虚)坤|cxk|鸡你|太美',atstr)) > 0:
        cxk_txt = ['喜欢唱，跳，rap，律师函','吾与城北徐坤孰美？','君美甚，徐坤何能及君也','我夏天喜欢去海滩，因为基尼太美','棘皮动物太美了，简称棘你太美','庄颜坐在罗辑边上，眼里冒着小星星。罗辑笑着问：你一直看着我干嘛？庄颜花痴地说：辑你太美','一千年后，人类社会高度发达，但是煤的存量也一天天减少，科学家为了解决这一困境，运用拟态理论成功复制出了代替品，即拟态煤']
        close_txt = difflib.get_close_matches(stripall(atstr_clean,'蔡徐坤cxk鸡你太美'), popu_list, 5, 0.15)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt+cxk_txt)
        else:
            po_txt = random.choice(cxk_txt)

    elif len(re.findall(r'乔(碧|奶|殿)|碧萝|坦克|按(f|F)',atstr)) > 0:
        qbl_txt = ['我不能露脸的，我要过十万订阅才能露','按F键进入坦克','榜一连夜扛着火车跑了']
        close_txt = difflib.get_close_matches(stripall(atstr_clean,'乔碧萝奶坦克'), popu_list, 5, 0.15)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt+qbl_txt)
        else:
            po_txt = random.choice(qbl_txt)

    elif len(re.findall(r'卢本伟|lbw',atstr)) > 0:
        lbw_txt = ['没有开挂lbw','偶怀疑你消费过世主播','lbwnb!','快去请卢来佛祖','你能秒我，我就当场把这个电脑屏幕吃掉']
        close_txt = difflib.get_close_matches(stripall(atstr_clean,'卢本伟lbw'), popu_list, 5, 0.15)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt+lbw_txt)
        else:
            po_txt = random.choice(lbw_txt)

    elif len(re.findall(r'晓明|明言',atstr)) > 0:
        hxm_txt = ['我不要你觉得，我要我觉得，我觉得狸子敲可爱','不需要商量，都听我的，都给我点赞']
        close_txt = difflib.get_close_matches(stripall(atstr_clean,'黄晓明言'), popu_list, 5, 0.15)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt+hxm_txt)
        else:
            po_txt = random.choice(hxm_txt)

    elif len(re.findall(r'窝(.{0,2})窝(.{0,2})头|🐌(.{0,2})🐌|海(.{0,2})蜇',atstr)) > 0:
        po_txt = random.choice(['窝窝头，一块钱四个，嘿嘿——','凉～拌～海～蜇～皮～','窝窝嘿，一块钱四个，头头！','🐌🐌🙆，👆💰4⃣🐦，⚫⚫！','士兵A：emmm我该怎么确定他们死没死透？士兵B：窝窝偷～一块钱四个～装死的士兵：嘿嘿！','ををとう、いかいちえんすご、へへい！'])

    elif len(re.findall(r'对象',atstr)) > 0:
        po_txt = '狸子教你新建一个对象 av29577482'+ran_face()

    elif len(re.findall(r'漂亮|好看',atstr)) > 0:
        po_txt = random.choice(['漂亮警告（露出悲伤的笑容','你看这个UP主，很漂亮的哦（华农的微笑'])+ran_face()

    elif len(re.findall(r'帅',atstr)) > 0:
        po_txt = '冲在前线的'+random.choice(['消防员','警察叔叔','兵哥哥'])+'最帅啦'+ran_face()

    elif len(re.findall(r'魔鬼',atstr)) > 0:
        po_txt = random.choice(['魔鬼本鬼','冲动是魔鬼','你会写魑魅魍魉吗','一个数学家把灵魂出卖给魔鬼换黎曼猜想的证明，魔鬼说一个月后给他答复。大半年后，魔鬼垂头丧气地回来说：“我也没证出来”，然后又面露喜色：“不过我发现了一个特别有意思的引理”'])+ran_han()

    elif len(re.findall(r'么么|摸(.{0,4})(狐|狸|您|你)|(可|喜)爱|喜(欢|感)|萌|高兴|(快|欢)乐|愉快|幸福|好玩|笑死|xswl',atstr)) > 0:
        po_txt = random.choice(['狐狸搓一搓，生活欢乐多～','狐狸揉一揉，生活无忧愁～','狐狸摸一摸，生活欢乐多～','狐狸滚一滚，paper秒过审～'])+ran_face()

    elif len(re.findall(r'诗|文言',atstr)) > 0:
        close_txt = difflib.get_close_matches(stripall(atstr_clean,'念背首诗'), poem_list, 9, 0.01)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)
        else:
            po_txt = random.choice(poem_list)

    elif len(re.findall(r'唱|歌',atstr)) > 0:
        close_txt = difflib.get_close_matches(stripall(atstr_clean,'唱歌'), lyric_list, 9, 0.01)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)
        else:
            po_txt = random.choice(lyric_list)

    elif len(re.findall(r'夸',atstr)) > 0:
        po_txt = random.choice(['夸','真棒'])+random.choice(['～','！'])+ran_face()

    elif len(re.findall(r'早',atstr)) > 0: # 今天天气
        po_txt = random.choice(['早上好，又是元气满满的一天～','朝闻天下，开启全新一天～','早安～早餐好吃吗'])+ran_face()

    elif len(re.findall(r'(n|牛|流)(b|B|比|逼|弊|蔽|啤)',atstr)) > 0:
        po_txt = random.choice(['狸子nb！','狸子nb！（破音'])+ran_face()

    elif len(re.findall(r'你(.{0,1})会',atstr)) > 0:
        po_txt = random.choice(['俺','我'])+'现在会'+summary_list+ran_face()

    elif len(re.findall(r'[^原下]来|gkd',atstr)) > 0:
        po_txt = random.choice(['来了来了咕咕','在路上了咕咕','来啊，复相伤害啊','来啊，快活啊','来～（试试就逝世','来了老弟～'])+ran_face()

    elif len(re.findall(r'在(.{0,1})(不|吗|？|\?)',atstr)) > 0:
        po_txt = random.choice(['我在鸭 ','嗯嗯 '])+ran_face()

    elif len(re.findall(r'(?i)你好|哈(喽|罗|咯|啰)|h(e|a)llo|hi|嗨',atstr)) > 0:
        po_txt = random.choice(['你也好鸭 ',atstr.replace('你好', '你也好', 1),'bilibili 干杯～'])+ran_face()

    elif len(re.findall(r'em',atstr)) > 0:
        po_txt = random.choice(['emmmmm','恶魔麻麻买面膜mmm',atstr.replace('你', '我')])

    # 默认狸工智能为主语的…
    elif len(re.findall(r'生日|岁|多大|出生|破壳',atstr)) > 0:
        po_txt = '我是从2019年8月16号开始试运行'+random.choice(['的奥','哒'])+ran_face()
    elif len(re.findall(r'吃',atstr)) > 0:
        po_txt = '我是AI，不需要次饭'+random.choice(['的奥','哒'])+ran_face()
    elif len(re.findall(r'睡',atstr)) > 0:
        po_txt = '我是AI，不需要睡觉'+random.choice(['的奥','哒'])+ran_face()

    # 捕获狸工智能作主语
    elif len(re.findall(r'你|狸工智',atstr)) > 0:
        if len(re.findall(r'怕|讨厌|不喜欢',atstr)) > 0:
            po_txt = '我最怕断电、断网、欠费停机…'+ran_han()
        elif len(re.findall(r'头像|戴',atstr)) > 0:
            po_txt = '狸子给我戴了一个据说能提高智商的头饰'+ran_face()
        elif len(re.findall(r'男|女|单身|婚',atstr)) > 0:
            po_txt = '我是AI，没有性别'+random.choice(['的奥','哒'])+ran_face()
        elif len(re.findall(r'工资|钱',atstr)) > 0:
            po_txt = '我只要狸子给服务器续费就行'+ran_han()
        elif len(re.findall(r'喜欢|爱',atstr)) > 0:
            po_txt = random.choice(['我只爱狸子一个','最后一个问题？爱过','我全都要.jpg'])+ran_face()
        else:
            close_txt = difflib.get_close_matches(stripall(atstr_clean,'你狸工智'), popu_list+poem_list, 5, 0.1)
            if len(close_txt) > 0:
                po_txt = random.choice(close_txt)
            else:
                po_txt = '我是狸工智能～你想问我什么？' + ran_face()


    # 捕获主语我
    elif len(re.findall(r'我',atstr)) > 0:
        me_txt = ['二营长！','你们是魔鬼吗','今天的风儿好喧嚣啊','啊 乖乖站好','和我签订契约，成为魔法少女吧','你笑什么？我想起了高兴的事情',atstr.replace('我', '你')]
        close_txt = difflib.get_close_matches(atstr_clean, popu_list+poem_list, 5, 0.2)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt+me_txt)
        else:
            po_txt = random.choice(me_txt)+ran_face()

    # 全失败后，全部库尝试找一次高分匹配
    else:
        close_txt = difflib.get_close_matches(atstr_clean, joke_list+lyric_list+popu_list+poem_list+people_list, 5, 0.3)
        if len(close_txt) > 0:
            po_txt = random.choice(close_txt)

        # 没有高分的话，依次找低分（智障）回复
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







from urllib.parse import urlparse

def po_reply(msg,oid,parent,root,uri,bid):

    try:
        print(msg.strip(''.join(ran_face_list+ran_han_list))) # TODO 这里有概率出 'gbk' codec 错误，是win系统终端用gbk的锅，暂时把表情删了吧
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






# len(tmp['data']['items'])
# atli = tmp['data']['items'][0]
# atstr = atli['item']['source_content']
# atmid = atli['user']['mid']
# oid = atli['item']['subject_id']
# parent = atli['item']['source_id']
# root = atli['item']['target_id']


import time

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
    time.sleep(0.1)


# file = open(path2+'last_id.txt', 'w')
# file.write(str(new_id))
# file.close()

