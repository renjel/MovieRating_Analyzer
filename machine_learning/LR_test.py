# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/20 10:46
# @IDE:         PyCharm
import json

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import redis

# 读取文件
data = pd.read_csv("movie_index(1).csv",header=0,)
pd.set_option('display.max_columns',None)
pd.set_option('display.width',1000)
# print(data.head())
# print(type(data["id"].values))
# for id0 in data["id"].values:
#     print(id0)
this_id = 30391241
print(data[data["id"] == this_id])

# print(data.loc[data["id"]==1291543])
# print(data[])

# 初始化redis连接
HOST = 'localhost'
PORT = '6379'
PASSWORD = '123waq'

r_db = redis.Redis(host=HOST,
                   port=PORT,
                   password=PASSWORD,
                   decode_responses=True,   # decode_responses=True，写入value中为str类型，否则为字节型
                   db='0')                  # 默认不写是db0

print(r_db.hget("movie_detail",this_id))

director_rate = 0
author_rate = 0
actor_rate = 0
movie_detail = json.loads(r_db.hget("movie_detail",this_id))
# 提取出director分
# 查找出本片导演
print(movie_detail["director"])
director_list = list(movie_detail["director"].keys())
# 根据导演id，查看该人相关联的电影
for direcort_id in director_list:
    celebrity_info = json.loads(r_db.hget("celebrity_info",direcort_id))
    print(celebrity_info)
