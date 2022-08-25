from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

template_id = os.environ["TEMPLATE_ID"]             # 模板ID
user_id = os.environ["USER_ID"]                     # 用户ID
userList = user_id.split(",")                           #把 user_id 转换成数组

today = datetime.now().strftime("%Y-%m-%d")         #今天的日期
start_date = os.environ['START_DATE']               #开始日期
city = os.environ['CITY']                           #城市
birthday = os.environ['BIRTHDAY']                   #生日

#
#
# app_id = "wxaa57ccc2ffea23bc"
# app_secret = "654f53177e70d14e25b19e764b9f2ba1"
#
# today = datetime.now().strftime("%Y-%m-%d")
# start_date = '2017-09-01'
# city = "武汉"
# birthday = '1999-07-10'
# user_id = "oV2R76PUmhE1KCiN1AZ_At9NQFhI,oV2R76KnAJd6LJFlRjOwpTd4QxzI"
# list = user_id.split(",")
# template_id = "4L7c64FszgKmFd5hlR5vyQYa4zAtcGMy9ws61W6biiQ"

td = datetime.strptime(today, "%Y-%m-%d")
sd = datetime.strptime(start_date, "%Y-%m-%d")
bd = datetime.strptime(birthday, "%Y-%m-%d")

toDate = str(td.month)+"月"+str(td.day)+"日"

def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], weather['high'], weather['low'], weather['wind']


def get_count():
    delta = td - sd
    return delta.days


def get_birthday():
    next_year = int(td.year) + 1
    nextBd = datetime.strptime(str(next_year) + "-" + str(bd.month) + "-" + str(bd.day), "%Y-%m-%d")  # 明年的生日
    thisBd = datetime.strptime(str(int(td.year)) + "-" + str(bd.month) + "-" + str(bd.day), "%Y-%m-%d")  # 今年的生日
    if thisBd == td:
        return "远方的我一直在掂念着你，祝你生日快乐。"
    elif td > thisBd:
        d = nextBd - td
        return "距离你的生日还有"+str(d.days)+"天"
    elif thisBd > td:
        d = thisBd - td
        return "距离你的生日还有"+str(d.days)+"天"


def get_qingShi():
    url = "http://api.tianapi.com/qingshi/index?key=5b6cd616d69d7560b1680d54abbaa82c"
    res = requests.get(url).json()
    qingShi = res['newslist'][0]
    return qingShi['content']


def get_saylove():
    url = "http://api.tianapi.com/saylove/index?key=5b6cd616d69d7560b1680d54abbaa82c"
    res = requests.get(url).json()
    saylove = res['newslist'][0]
    return saylove['content']


def get_words():
    url = "https://api.shadiao.pro/chp"
    res = requests.get(url).json()
    caiHongPi = res['data']
    return caiHongPi['text']


# 判断是否为质数
def zhiShu(num):
    if num > 1:
        # 查看因子
        for i in range(2, num):
            if (num % i) == 0:
                # print(num, "不是质数")
                # print(i, "乘于", num // i, "是", num)
                return 0
        else:
            # print(num, "是质数")
            return 1

    # 如果输入的数字小于或等于 1，不是质数
    else:
        # print(num, "不是质数")
        return 0


def say():
    num = random.randint(1, 10)

    if zhiShu(num) == 1:
        return get_words()
    elif num % 2 == 0:
        return get_qingShi()
    else:
        return get_saylove()


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, high, low, wind = get_weather()

data = {
    "date": {"value": toDate},
    "city": {"value": city},
    "weather": {"value": wea},
    "high": {"value": str(high)},
    "low": {"value": str(low)},
    "wind": {"value": str(wind)},
    "love_days": {"value": get_count()},
    "birthday_left": {"value": str(get_birthday())},
    "words": {"value": say(),
              "color": get_random_color()}
}


for i in userList:
    res = wm.send_template(i, template_id, data)



#
# print(
#     "天气" + wea + "\n" +
#     "最高气温：" + str(high) + "\n" +
#     "最低气温：" + str(low) + "\n" +
#     "wind" + str(wind) + "\n" +
#     "认识的天数：", get_count() + "\n" +
#     get_birthday() + "\n" +
#     say()
# )



# if __name__ == '__main__':
#
#     print(get_count())

# def bo():
#     next_year = int(td.year) + 1
#     nextBd = datetime.strptime(str(next_year) + "-" + str(bd.month) + "-" + str(bd.day),"%Y-%m-%d")  # 明年的生日
#     thisBd = datetime.strptime(str(int(td.year)) + "-" + str(bd.month) + "-" + str(bd.day),"%Y-%m-%d")  # 今年的生日
#     print(nextBd)
#     print(thisBd)
#
#     if thisBd == td:
#         return "生日快乐"
#     elif td > thisBd:
#         d = nextBd - td
#         return "距离生日还有：" + str(d.days) + "天"
#     elif thisBd > td:
#         d = thisBd - td
#         return "距离生日还有：" + str(d.days) + "天"
