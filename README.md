# BiliResp

这里是狸工智能的艾特回复程序，用法是在B站任意评论区艾特：狸工智能，后面加上带关键词的语句

注意：

- 在动态或者简介里的艾特暂时回复不了（格式不一样，暂时懒得研究）
- 目前的状态为每2分钟检查一次B站收到的艾特消息，每次检查最新的20个
  - 如果某两分钟的艾特数超过20个，旧的消息就不会得到回复
- 回复消息过频繁会被系统ban，所以最好不要短时间内艾特太多
- 如果回复发送失败，狸工智能不会再试，所以如果你2分钟后还没收到回复，请等一段时间后重新再艾特
- 如果长期得不到回复，甚至连更新专栏都中断了，这可能是cookie过期~~或服务器炸了~~，请艾特狸子LePtC前去修复


## 已实现回复的关键词

示例 | 正则 | 回复
------------ | ------------- | -------------
用法 | `用法\|指南\|说明\|帮助\|(怎么\|可以)(问\|查)\|你(.{0,2})家\|help\|F1\|f1` | 本项目网址
卖萌 | `卖(.{0,3})萌` | 狸子敲可爱
狐狸叫 | `狸(.{0,3})叫\|fox(.{0,3})say` | 嘤嘤嘤



## 开发者

对于一些简单直接（不需要查数据库）的回复，大家可以来跟狸子一起开发～

举个例子，用正则表达式判断艾特消息中是否有“卖萌”字样

`if len(re.findall(r'卖(.?)萌',atstr)) > 0:`

然后回复随机组合句

`po_reply('狸子'+random.choice(['敲','敲极'])+random.choice(['可','阔'])+'爱～',oid,parent,root)`

怎么样，是不是敲级简单？

大家在 python 中测试时（推荐用 jupyter）自己把 `atstr` 给定义了就可以测试输入输出了。如果想做线上测试的话，用你自己帐号的 `cookie` 奥 \_Σ:з」∠)シ\_



## 狸子的 TODO

- 查我排名
- 查谁谁谁排名
- 申请收录我
- 申请收录谁谁谁
- 申请收id888888


## 开发日志

- 20190818
  - 初次尝试回复卖萌
  - 加入狐狸叫和帮助

