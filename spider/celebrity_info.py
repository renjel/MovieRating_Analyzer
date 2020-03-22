# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/18 14:22
# @IDE:         PyCharm

import datetime
import re
from time import sleep

import requests
import json
from lxml import etree
import redis
import random

def celebrity_map(tag_in):
    if tag_in in ("导演","编剧","演员"):
        if tag_in == "导演":
            tag_out = "director"
        elif tag_in == "编剧":
            tag_out = "author"
        elif tag_in == "演员":
            tag_out = "actor"
        return tag_out
    else:
        return tag_in

def get_celebrity_info(celebrity_id):
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

    celebrity_tag = ["导演","编剧","演员"]

    url = "https://movie.douban.com/celebrity/" + str(celebrity_id) + "/movies?sortby=vote&format=text"
    if random.randint(0, 99) < 50:
        req = requests.get(url, headers=headers)
    else:
        req = requests.get(url, headers=headers2)
    html = etree.HTML(req.text)
    celebrity_dict = {}
    for i in range(1,100):
        xpath_url = '//*[@id="content"]/div/div[1]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/a/@href'
        xpath_role = '//*[@id="content"]/div/div[1]/div[2]/table/tbody/tr[' + str(i) + ']/td[4]/text()'
        # print(i)
        try:
            roles = html.xpath(xpath_role)[0]
        except Exception as e1:
            # print(e1)
            continue
        if "/" in roles:
            for role in roles.split("/"):
                for tag in celebrity_tag:
                    if tag in role:
                        role = tag
                if celebrity_dict.get(celebrity_map(role.strip())) is None:
                    celebrity_dict[celebrity_map(role.strip())] = [html.xpath(xpath_url)[0].split("/")[4]]
                else:
                    if html.xpath(xpath_url)[0].split("/")[4] in celebrity_dict[celebrity_map(role.strip())]:
                        continue
                    else:
                        celebrity_dict[celebrity_map(role.strip())].append(html.xpath(xpath_url)[0].split("/")[4])
        else:
            for role in roles.split("-"):
                for tag in celebrity_tag:
                    if tag in role:
                        role = tag
                if celebrity_dict.get(celebrity_map(role.strip())) is None:
                    celebrity_dict[celebrity_map(role.strip())] = [html.xpath(xpath_url)[0].split("/")[4]]
                else:
                    if html.xpath(xpath_url)[0].split("/")[4] in celebrity_dict[celebrity_map(role.strip())]:
                        continue
                    else:
                        celebrity_dict[celebrity_map(role.strip())].append(html.xpath(xpath_url)[0].split("/")[4])
    # print(json.dumps(celebrity_dict,ensure_ascii=False))
    celebrity_str = json.dumps(celebrity_dict,ensure_ascii=False)


    # 初始化redis连接
    HOST = 'localhost'
    PORT = '6379'
    PASSWORD = '123waq'

    r_db = redis.Redis(host=HOST,
                       port=PORT,
                       password=PASSWORD,
                       decode_responses=True,   # decode_responses=True，写入value中为str类型，否则为字节型
                       db='0')                  # 默认不写是db0


    r_db.hset("celebrity_info",celebrity_id,celebrity_str)
    # print(r_db.hget("celebrity_info",celebrity_id))
    # print(type(json.loads(r_db.hget("celebrity_info",celebrity_id))))
    print("新加载入库，内容为：" + r_db.hget("celebrity_info",celebrity_id))
    sleep(5)

if __name__ == "__main__":
    get_celebrity_info(1048026)

