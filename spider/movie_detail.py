# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/17 15:50
# @IDE:         PyCharm
import datetime
import re
import requests
import json
from lxml import etree
import redis

# 添加请求头
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}

url = "https://movie.douban.com/subject/30391241/"
req = requests.get(url, headers=headers)
html = etree.HTML(req.text)
# xpath = '//*[@id="info"]/span[1]/span[3]/a/text()'
xpath = '/html/head/script[8]/text()'
# print(re.text)
movie_dict = json.loads(html.xpath(xpath)[0])
print(json.loads(html.xpath(xpath)[0]))
duration = int(re.findall(r'\d+',movie_dict["duration"])[0]) * 60 + int(re.findall(r'\d+',movie_dict["duration"])[1])
movie_detail = {"id":movie_dict["url"].split("/")[2],"name":movie_dict["name"],"datePublished":movie_dict["datePublished"],"genre":movie_dict["genre"],
                "duration":duration,"ratingCount":movie_dict["aggregateRating"]["ratingCount"],"ratingValue":movie_dict["aggregateRating"]["ratingValue"]}

director_dict = {}
for director in movie_dict["director"]:
    # print(director)
    director_dict[director["url"].split("/")[2]] = director["name"]
movie_detail["director"] = director_dict

author_dict = {}
for author in movie_dict["author"]:
    author_dict[author["url"].split("/")[2]] = author["name"]
movie_detail["author"] = author_dict

actor_dict = {}
for actor in movie_dict["actor"]:
    actor_dict[actor["url"].split("/")[2]] = actor["name"]
movie_detail["actor"] = actor_dict



rat_list = []
for i in range(1,6):
    xpath_rat = '//*[@id="interest_sectl"]/div[1]/div[3]/div[' + str(i) + ']/span[2]/text()'
    rat_list.append(html.xpath(xpath_rat)[0])

movie_detail["ratingDetail"] = rat_list

movie_detail["content"] = html.xpath('//*[@id="link-report"]/span/text()')[0].strip("\n").strip()

movie_str = json.dumps(movie_detail,ensure_ascii=False)
print(json.dumps(movie_detail))

print(type(json.dumps(movie_detail)))

# 初始化redis连接
HOST = 'localhost'
PORT = '6379'
PASSWORD = '123waq'

r_db = redis.Redis(host=HOST,
                   port=PORT,
                   password=PASSWORD,
                   decode_responses=True,   # decode_responses=True，写入value中为str类型，否则为字节型
                   db='0')                  # 默认不写是db0


r_db.hset("movie_detail",movie_detail["id"],movie_str)
print(r_db.hget("movie_detail",movie_detail["id"]))
print(type(json.loads(r_db.hget("movie_detail",movie_detail["id"]))))
