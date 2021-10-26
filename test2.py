# -*- coding: utf-8 -*-
import json
import requests
import time
import hashlib
import string
import random
import sys
 
def main_handler():
    buildHearders()
    # 签到
    signResult = sign()
    # 游戏信息
    totalSignDay = getTotalSignDay()["data"]
    totalSignDay = totalSignDay["total_sign_day"]
    gameInfo = getGameInfo()["data"]["list"][0]
    signInfo = getSignInfo()["data"]
    award = signInfo["awards"][totalSignDay - 1]
    # 方糖message内容，请不要格式化这段字符串
    message = '''>{}
 
##### 游戏昵称：{}
##### 冒险等级：{}
##### 签到结果：{}
##### 签到奖励：{} x {}
##### {}月累计签到：**{}** 天'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+28800)), gameInfo["nickname"],
                                 gameInfo["level"],
                                 signResult['message'], award['name'], award['cnt'], signInfo["month"],
                                 totalSignDay)
    return notify(message)
 
 
# 设置请求头
def buildHearders():
    headers["Cookie"] = cookie
    headers["x-rpc-device_id"] = device_id
    headers["Host"] = "api-takumi.mihoyo.com"
    headers["Content-type"] = "application/json;charset=utf-8"
    headers["Accept"] = "application/json, text/plain, */*"
    headers["x-rpc-client_type"] = "5"
    headers["x-rpc-app_version"] = app_version
    headers["DS"] = getDS()
 
def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()
 
 
def getDS():
    # n = 'cx2y9z9a29tfqvr1qsq6c7yz99b5jsqt' # v2.2.0 @Womsxd   
    n = 'h8w582wxwgqvahcdkpvdhbh2w9casgfl' # v2.3.0 web @povsister & @journey-ad   
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return "{},{},{}".format(i, r, c)
 
# 签到
def sign():
    signUrl = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign"
    param = {"act_id": act_id, "region": region, "uid": uid}
    result = requests.request("POST", signUrl, headers=headers, data=json.dumps(param))
    print(result.text)
    return json.loads(result.content)
 
 
# 获取签到信息
def getSignInfo():
    url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id={}"
    userInfoResult = requests.get(url.format(act_id), headers=headers)
    return json.loads(userInfoResult.content)
 
 
# 获取签到天数
def getTotalSignDay():
    url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?region={}&act_id={}&uid={}"
    userInfoResult = requests.get(url.format(region, act_id, uid), headers=headers)
    print(userInfoResult.text)
    return json.loads(userInfoResult.content)
 
 
# 获取游戏信息
def getGameInfo():
    url = "https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn"
    userInfoResult = requests.get(url, headers=headers)
    return json.loads(userInfoResult.content)
 
 
# 微信推送
def notify(message):
    print(message)
 
app_version = "2.3.0"
act_id = "e202009291139501"
region = "cn_qd01"
uid = "500043656"
#cookie = "_MHYUUID=25d849c6-f8d8-445c-a20a-1a508361f7bd; _ga=GA1.1.215929378.1634657266; ltoken=4Vp3v5H15XtjfN9Qjbni0r15h5hjvA7prHNfEIiK; ltuid=75352370; login_ticket=vixCbG86ZNXOau5d1AOlVcYxF37kyb9xi0mszXPy; account_id=75352370; cookie_token=5UyBSSXKHh7rfeVHtrGPuXbCQKJGlgjyB3jtug3i; _ga_KJ6J9V9VZQ=GS1.1.1635048729.3.1.1635049120.0"
cookie = sys.argv[1]
print(sys.argv[1])
# 设备号随意，但不能为空
device_id = "94581081EDD446EFAA3A45B8CC636CCF"
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.3.0"
}
main_handler()