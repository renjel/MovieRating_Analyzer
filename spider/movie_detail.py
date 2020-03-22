# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/17 15:50
# @IDE:         PyCharm
import datetime
import re
from time import sleep
import random
import requests
import json
from lxml import etree
import redis

# 加入随机数来决定使用的cookie



def get_movie_detail(movie_id):
    # 添加请求头
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Cookie": '_vwo_uuid_v2=DF1CD1D02C1F8E768DBF47BF79A9F1E74|b12b5befc6df7585392eb4a002c4cf90; douban-fav-remind=1; trc_cookie_storage=taboola%2520global%253Auser-id%3D0a22c941-ee80-46a4-8a54-4d536d22ac19-tuct42dacfe; __gads=ID=3eea0cf197f18381:T=1572193084:S=ALNI_MZEvinttZ6YoG1H45Vo0sCZPtiCXw; ll="118201"; bid=llzh4k6OdTQ; __yadk_uid=PXtKaw8K4PbibbDwnJPNql0K8gNSek3c; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21387; __utmz=30149280.1584629577.16.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1584630785.13.11.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; __utma=30149280.1436318017.1543845487.1584802018.1584872463.18; __utmc=30149280; __utma=223695111.1469249451.1543845487.1584802018.1584872463.15; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1584879059%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=ffa48de66b2ed73f.1543845486.16.1584879059.1584874662.; _pk_ses.100001.4cf6=*; dbcl2="213873128:4KaTmtgwOO8"'
    }

    headers2 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }

    url = "https://movie.douban.com/subject/" + str(movie_id) + "/"
    if random.randint(0,99) < 50:
        req = requests.get(url, headers=headers)
    else:
        req = requests.get(url, headers=headers2)
    html = etree.HTML(req.text)
    # xpath = '//*[@id="info"]/span[1]/span[3]/a/text()'
    xpath = '/html/head/script[8]/text()'
    # print(re.text)
    print(html.xpath(xpath)[0])
    print(html.xpath(xpath)[0].replace("\n","",144))
    movie_dict = json.loads(html.xpath(xpath)[0].replace("\n",""))
    # print(movie_dict)
    # print(movie_dict["duration"])
    try:
        duration = int(re.findall(r'\d+', movie_dict["duration"])[0]) * 60 + int(
            re.findall(r'\d+', movie_dict["duration"])[1])
    except Exception as e3:
        # print(e3)
        duration = 0
    movie_detail = {"id": movie_dict["url"].split("/")[2], "name": movie_dict["name"],
                    "datePublished": movie_dict["datePublished"], "genre": movie_dict["genre"],
                    "duration": duration, "ratingCount": movie_dict["aggregateRating"]["ratingCount"],
                    "ratingValue": movie_dict["aggregateRating"]["ratingValue"]}

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
    try:
        for i in range(1, 6):
            xpath_rat = '//*[@id="interest_sectl"]/div[1]/div[3]/div[' + str(i) + ']/span[2]/text()'
            rat_list.append(html.xpath(xpath_rat)[0])
    except Exception as e1:
        print(e1)

    movie_detail["ratingDetail"] = rat_list
    try:
        movie_detail["content"] = html.xpath('//*[@id="link-report"]/span/text()')[0].strip("\n").strip()
    except Exception as e2:
        # print(e2)
        movie_detail["content"] = ""

    movie_str = json.dumps(movie_detail, ensure_ascii=False)
    # print(json.dumps(movie_detail))

    # print(type(json.dumps(movie_detail)))

    # 初始化redis连接
    HOST = 'localhost'
    PORT = '6379'
    PASSWORD = '123waq'

    r_db = redis.Redis(host=HOST,
                       port=PORT,
                       password=PASSWORD,
                       decode_responses=True,  # decode_responses=True，写入value中为str类型，否则为字节型
                       db='0')  # 默认不写是db0

    r_db.hset("movie_detail", movie_detail["id"], movie_str)
    # print(r_db.hget("movie_detail", movie_detail["id"]))
    # print(type(json.loads(r_db.hget("movie_detail", movie_detail["id"]))))
    print("新加载入库，内容为：" + r_db.hget("movie_detail", movie_id))
    sleep(5)
    # return json.loads(r_db.hget("movie_detail", movie_detail["id"]))



if __name__ == "__main__":
    get_movie_detail(1531948)


