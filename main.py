from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

# 微信测试号的 app_id
app_id = os.environ["APP_ID"]

# 微信测试号的 app_secret
app_secret = os.environ["APP_SECRET"]

# 模板ID
template_id = os.environ["TEMPLATE_ID"]

# 用户ID
user_id = os.environ["USER_ID"]

# 天行API我的密钥KEY
txApiKey = os.environ["TXAPI_ID"]

# 把 user_id 以英文逗号分隔并转换成数组
userList = user_id.split(",")

# 今天的日期
today = datetime.now().strftime("%Y-%m-%d")

# 开始日期
start_date = os.environ['START_DATE']

# 城市
city = os.environ['CITY']

# 生日
birthday = os.environ['BIRTHDAY']



# 时间格式化统一
td = datetime.strptime(today, "%Y-%m-%d")
sd = datetime.strptime(start_date, "%Y-%m-%d")
bd = datetime.strptime(birthday, "%Y-%m-%d")

# 自动获取今天的时间，转换成str；格式如：8月10日
toDate = str(td.month) + "月" + str(td.day) + "日"

# td.weekday()：获取今日是一周中的第几天（0-6），将其转换成星期几
week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
toWeek = week_list[td.weekday()]


# 获取墨迹天气的API
def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    # 返回数据依次为：天气“晴”，当前气温，空气湿度，最高气温，最低气温，风力等级“东风4级”，pm2.5，空气质量
    return str(weather['weather']), str(round(weather['temp'])), str(weather['humidity']), str(
        round(weather['high'])), str(round(weather['low'])), str(weather['wind']), str(round(weather['pm25'])), str(weather['airQuality'])


########################################################################################################################
# 【START】------------------可选
# 获取情诗API
# url 的值为：
# {
#   "code":200,
#   "msg":"success",
#   "newslist":[
#       {
#           "content":"可怜无定河边骨，犹是春闺梦裏人。",
#           "source":"陇西行",
#           "author":"陈陶"
#       }
#   ]
# }
def get_qingShi():
    # "http://api.tianapi.com/qingshi/index" 替换为自己申请的API地址
    # 请求示例：http://api.tianapi.com/qingshi/index?key=APIKEY
    
    url = "http://api.tianapi.com/qingshi/index?key=" + txApiKey
    res = requests.get(url).json()
    qingShi = res['newslist'][0]
    return qingShi['content']


# 情话
def get_saylove():
    # "http://api.tianapi.com/saylove/index" 替换为自己申请的接口地址
    url = "http://api.tianapi.com/saylove/index?key=" + txApiKey
    res = requests.get(url).json()
    saylove = res['newslist'][0]
    return saylove['content']
# 【END】

# 彩虹屁
def get_words():
    # 开源API
    url = "https://api.shadiao.pro/chp"
    res = requests.get(url).json()
    caiHongPi = res['data']
    return caiHongPi['text']

# 【START】------------------可选
#PS：如果只用 get_words() 开源API则不需要以下判断，将 data 里的 say()替换成 get_words()
# 判断是否为质数
# 有多个不同总类de语句输出API，做个判断，是质数返回 1
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

# 随机输出不同类型的语句
def say():
    # 取包括1-10的随机整数
    num = random.randint(1, 10)
    # 如果是质数（2，3，5，7）
    if zhiShu(num) == 1:
        # 输出彩虹屁API
        return get_words()
    # 如果是偶数
    elif num % 2 == 0:
        # 输出情诗API
        return get_qingShi()
    else:
        # 其他情况输出情话API
        return get_saylove()
# 【END】


########################################################################################################################

# 计算从指定日期开始已经过了多少天
def get_count():
    delta = td - sd
    return delta.days


# 判断今日是否是其生日
def get_birthday():
    next_year = int(td.year) + 1
    nextBd = datetime.strptime(str(next_year) + "-" + str(bd.month) + "-" + str(bd.day), "%Y-%m-%d")  # 明年的生日
    thisBd = datetime.strptime(str(int(td.year)) + "-" + str(bd.month) + "-" + str(bd.day), "%Y-%m-%d")  # 今年的生日
    if thisBd == td:
        return "远方的我一直在掂念着你，祝你生日快乐。"
    elif td > thisBd:
        d = nextBd - td
        return "距离你的生日还有" + str(d.days) + "天"
    elif thisBd > td:
        d = thisBd - td
        return "距离你的生日还有" + str(d.days) + "天"


# 随机生成颜色
def get_random_color():
    color = "#%06x" % random.randint(0, 0xFFFFFF);
    print(color)
    return color


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temp, humidity, high, low, wind, pm25, airQuality = get_weather()

# 将数据打包成JSON格式
data = {
    "date": {
        "value": toDate + " " + toWeek,
        "color": get_random_color()
    },
    "city": {
        "value": city
    },
    "weather": {
        "value": wea,
        "color": get_random_color()
    },
    "temp": {
        "value": temp + " ℃",
        "color": get_random_color()
    },
    "humidity": {
        "value": humidity,
        "color": get_random_color()
    },
    "high": {
        "value": high + " ℃",
        "color": get_random_color()
    },
    "low": {
        "value": low + " ℃",
        "color": get_random_color()
    },
    "wind": {
        "value": wind,
        "color": get_random_color()
    },
    "pm25": {
        "value": pm25,
        "color": get_random_color()
    },
    "airQuality": {
        "value": airQuality,
        "color": get_random_color()
    },
    "love_days": {
        "value": get_count(),
        "color": get_random_color()
    },
    "birthday_left": {
        "value": str(get_birthday()),
        "color": get_random_color()
    },
    "words": {
        "value": "“ " + say() + " ”",   # 只使用彩虹屁 API 直接将 say() 替换为 get_words()
        "color": get_random_color()  # 给文字赋予随机颜色
    }
}

for i in userList:
    # 将数据携带给微信模板并指定用户发送
    wm.send_template(i, template_id, data)
