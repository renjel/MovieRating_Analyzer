# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/18 16:12
# @IDE:         PyCharm

import datetime
import re
import requests
import json
from lxml import etree
import redis
import html

# 添加请求头
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}



url = "https://maoyan.com/query?kw=战狼2"
req = requests.get(url, headers=headers)
html0 = etree.HTML(req.text)
url_movie = html0.xpath('//*[@id="app"]/div/dl/dd/div[2]/a/@href')[0]
print(url_movie)

url_bxo = "https://maoyan.com" + url_movie
req = requests.get(url_bxo, headers=headers)
html0 = etree.HTML(req.text)
print(req.text)
box_office = html0.xpath("/html/body/div[3]/div/div[2]/div[3]/div[2]/div/span[1]/text()")[0]
print(box_office)
if "&#xf412" in box_office:
    print("111")


if box_office != "暂无":
    print("yes")
    print(box_office.replace('.','').replace(';', '').replace('&#x', '\\u').encode('utf-8').decode('unicode_escape'))
    # print(html.unescape("&#xf412;&#xec5a;&#xf5a5;&#xf261;"))

