# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/18 14:22
# @IDE:         PyCharm

import datetime
import re
import requests
import json
from lxml import etree
import redis

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


# 添加请求头
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}

celebrity_id = 1386475
celebrity_tag = ["导演","编剧","演员"]

url = "https://movie.douban.com/celebrity/" + str(celebrity_id) + "/movies?sortby=vote&format=text"
req = requests.get(url, headers=headers)
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
print(json.dumps(celebrity_dict,ensure_ascii=False))
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
print(r_db.hget("celebrity_info",celebrity_id))
print(type(json.loads(r_db.hget("celebrity_info",celebrity_id))))