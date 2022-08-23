from datetime import date, datetime
#import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random


today = datetime.now()
todays = today.strftime('%Y-%m-%d %A') 


city = os.environ['CITY']
gaokao = os.environ['GAOKAO']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
#user_ids = [os.environ["USER_ID_1"], os.environ["USER_ID_2"]]
template_id = os.environ["TEMPLATE_ID"]

#city = '曹县'
# today = datetime.now()
# todays = today.strftime('%Y-%m-%d %A')
#gaokao = '06-07'

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

#英语一句话
def One_English():
    English_api = 'http://api.tianapi.com/ensentence/index?key=a3837d06c106a70ac573d583e6569795'
    English_res = requests.get(English_api)
    English_data = English_res.json()['newslist'][0]
    return English_data['en'], English_data['zh']

#天气
def get_weather():
    weather_api = 'http://api.tianapi.com/tianqi/index?key=a3837d06c106a70ac573d583e6569795&city='+ city
    weather_res = requests.get(weather_api)
    weather_data = weather_res.json()['newslist'][0]
    return weather_data


def get_gaokao():
  next = datetime.strptime(str(date.today().year) + "-" + gaokao, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/pyq")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

weather_data = get_weather()
en, zh = One_English()

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
data = {"date":{"value":todays, "color":get_random_color()}, "city":{"value":city}, "weather":{"value": weather_data['weather']},"min_temperature":{"value":weather_data['lowest'],"color":"#7FBA00"},"max_temperature":{"value":weather_data['highest'], "color":"#F25022"}, "pop":{"value":weather_data['pop']+'%'},"tips":{"value":weather_data['tips'], "color":get_random_color()},"birthday":{"value":get_gaokao(),"color":"#FF0000"},"note":{"value":get_words(), "color":get_random_color()},"note_en":{"value":en, "color":get_random_color()},"note_th":{"value":zh, "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)

