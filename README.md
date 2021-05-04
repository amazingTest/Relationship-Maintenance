# Relationship-Maintenance

## 项目背景

不知道有没有人和我一样，自从脱单后，会和另一半比谁先打卡（下午 5 点 20 的消息推送...），会突然被问今天是在一起多少天了
（有时候一下子确实没算出来...），会用彼此的生日数字买彩票（然后忘记去看中没中...）

基于以上原因，此项目诞生了...

本项目使用了史上最稳的微信消息推送方式（完全不会有任何封号等风险）

同时，本项目支持自定义消息定时发送配置，并内置了许多让感情升温的暖心语句。

希望世间有情人长长久久！

（单身的朋友也无需气馁, 先把此项目安排上，早日拿下心上人！）

## 功能介绍

+ 自定义微信消息推送

## 使用

### 安装依赖

    pip install -r requirements.txt
    
### 消息推送配置
    
本项目采用了企业微信推送消息到微信（个人微信也能注册，无需认证，消息能直接在微信看到）
    
1. 首先需要 [用电脑打开企业微信官网，注册一个企业](https://work.weixin.qq.com/)

2. 注册成功后，点「管理企业」进入管理界面，选择「应用管理」 → 「自建」 → 「创建应用」

3. 创建完成后进入应用详情页，可以得到应用ID ( agentid )，应用Secret ( secret )

4. 进入「我的企业」页面，拉到最下边, 获取企业ID (corpid)

最后一步，将上面获得的 agentid，secret，corpid 写入 config/messenger.json 中就大功告成了。

#### 例子
    
    examples/config/messenger.json
    
    [{
      "channel": "enterprise_we_chat_app",
      "payload": {
          "agentid": "1000001",
          "corpid": "wweb6a6b9523f30fa4",
          "secret": "JF1BC4UvyEW8ZepkVfsg_AlAgjqFpNIslA_hUD78Dso"
      }
    }]


### 定时任务配置

用于创建定时任务，定时向微信推送消息。

在 config/cron.json 中进行配置

#### 例子
    
    examples/config/cron.json
    
    [{
	"mission": {
		"name": "lover_greeting",
		"payload": {
			"title": "宝贝～ 起床啦～",
			"begin_date": "2021-11-10",
            "greeting_type": "morning"
		}
	},
	"cron": "00 08 * * *",
	"messenger": "enterprise_we_chat_app"
    }, {
        "mission": {
            "name": "lover_greeting",
            "payload": {
                "title": "宝贝～ 中午啦～",
                "greeting_type": "normal"
            }
        },
        "cron": "00 12 * * *",
        "messenger": "enterprise_we_chat_app"
    },
    {
        "mission": {
            "name": "lover_greeting",
            "payload": {
                "title": "520 ！准时打卡！",
                "content": "准时不！",
            }
        },
        "cron": "20 17 * * *",
        "messenger": "enterprise_we_chat_app"
    }]

例子中共有 3 个定时消息推送任务:

1. 早上 8 点推送一条消息:

        宝贝～ 起床啦～ 今天我们在一起 184 天了～
    
        早安！当你睁开双眼，祝福已飞到你面前，带着快乐的旋律，愉悦的心态，滚滚的财源，甜蜜的浪漫和美妙的生活伴你度过美好的一天！

2. 中午 12 点推送一条消息:

        宝贝～ 中午啦～
    
        my baby，虽然情人节时咱们不能在一起过，但是我要你知道，我的心从来没有走远...爱你!
    
    
3. 下午 5 点 20 推送一条消息:

        520 ！准时打卡！
    
        准时不！

#### 参数解释: 

payload 中的 begin_date(opt) 代表的是开始在一起的时间，用于计算在一起的时长;

payload 中 title(opt) 表示推送的标题;

payload 中 greeting_type(opt) 表示 lover_greeting 推送的类型（会随机在 config/builtin_sentences.json 中选择一条作为 content);
（若在 payload 设置 content(opt) 值则会覆盖 greeting_type 参数产生的效果）


### 运行程序

    python3 main.py
    
### 待完成的功能

+ 彩票消息推送机器人
+ 天气预报推送机器人
+ 各种第三方消息推送机器人...




