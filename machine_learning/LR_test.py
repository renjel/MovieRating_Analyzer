# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/20 10:46
# @IDE:         PyCharm
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import redis

from spider.celebrity_info import get_celebrity_info
from spider.movie_detail import get_movie_detail

# 读取文件
data = pd.read_csv("movie_index(1).csv", header=0, )
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# print(data.head())
# print(type(data["id"].values))
# for id0 in data["id"].values:
#     print(id0)
this_id = 1291543
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
                   decode_responses=True,  # decode_responses=True，写入value中为str类型，否则为字节型
                   db='0')  # 默认不写是db0


if r_db.hget("movie_detail", this_id) is None:
    # print(movie_id)
    get_movie_detail(this_id)
print(r_db.hget("movie_detail", this_id))
director_rate = 0
author_rate = 0
actor_rate = 0

movie_detail = json.loads(r_db.hget("movie_detail", this_id))
this_genre = movie_detail["genre"]

'''
    提取出role分
'''
def get_role_rating(movie_detail,role):
    # 查找出本片任职
    print(movie_detail[role])
    role_list = list(movie_detail[role].keys())
    role_rating_list = []
    # 根据任职id，查看该人相关联的电影
    for role_id in role_list:
        # 查看该人是否存在，不存在则获取入库
        if r_db.hget("celebrity_info", role_id) is None:
            print(role_id)
            get_celebrity_info(role_id)
        celebrity_info = json.loads(r_db.hget("celebrity_info", role_id))
        # print(celebrity_info)
        # 先检查电影是否存在，不存在则将电影添加到库里。
        movie_list = []
        for role0 in celebrity_info:
            for movie_id in celebrity_info[role0]:
                if movie_id in movie_list:
                    continue
                else:
                    movie_list.append(movie_id)
        for movie_id in movie_list:
            if r_db.hget("movie_detail", movie_id) is None:
                print(movie_id)
                get_movie_detail(movie_id)
        # 根据题材计算出该任职的任职分
        key_rating_sameGenre_list = []
        key_rating_noSameGenre_list = []
        other_rating_sameGenre_list = []
        other_rating_noSameGenre_list = []
        for movie_id in celebrity_info[role]:
            movie = json.loads(r_db.hget("movie_detail", movie_id))
            # print("name:" + movie["name"] + " genre:" + ",".join(movie["genre"]) + " rating:" + movie["ratingValue"])
            if movie["ratingValue"] == "":
                continue
            if len(list(set(this_genre).intersection(set(movie["genre"])))) == 0:
                key_rating_noSameGenre_list.append(float(movie["ratingValue"]))
            else:
                key_rating_sameGenre_list.append(float(movie["ratingValue"]))
        if len(key_rating_noSameGenre_list) == 0:
            key_rating_noSameGenre_list = [0]
        if len(key_rating_sameGenre_list) == 0:
            key_rating_sameGenre_list = [0]
        key_rating = np.mean(key_rating_noSameGenre_list) * 0.2 + np.mean(key_rating_sameGenre_list) * 0.8
        for oter_role in celebrity_info:
            for movie_id in celebrity_info[oter_role]:
                movie = json.loads(r_db.hget("movie_detail", movie_id))
                # print("name:" + movie["name"] + " genre:" + ",".join(movie["genre"]) + " rating:" + movie["ratingValue"])
                if movie["ratingValue"] == "":
                    continue
                if len(list(set(this_genre).intersection(set(movie["genre"])))) == 0:
                    other_rating_noSameGenre_list.append(float(movie["ratingValue"]))
                else:
                    other_rating_sameGenre_list.append(float(movie["ratingValue"]))
        if len(other_rating_noSameGenre_list) == 0:
            other_rating_noSameGenre_list = [0]
        if len(other_rating_sameGenre_list) == 0:
            other_rating_sameGenre_list = [0]
        other_rating = np.mean(other_rating_noSameGenre_list) * 0.2 + np.mean(other_rating_sameGenre_list) * 0.8
        role_rating = key_rating * 0.8 + other_rating * 0.2
        # print(key_rating_sameGenre_list)
        # print(key_rating_noSameGenre_list)
        # print(other_rating_sameGenre_list)
        # print(other_rating_noSameGenre_list)
        # print(role_rating)
        role_rating_list.append(role_rating)
    # print(role_rating_list)
    return role_rating_list

# 提取导演分
print("提取导演分-------------------------------------------------------------------------------------")
director_rating_list = get_role_rating(movie_detail,"director")
movie_role_rating = np.mean(director_rating_list)
print(director_rating_list)
print(movie_role_rating)

# 提取编剧分
print("提取编剧分-------------------------------------------------------------------------------------")
author_rating_list = get_role_rating(movie_detail,"author")
movie_role_rating = np.mean(author_rating_list)
print(author_rating_list)
print(movie_role_rating)

# 提取演员分
print("提取演员分-------------------------------------------------------------------------------------")
actor_rating_list = get_role_rating(movie_detail,"actor")
movie_role_rating = np.mean(actor_rating_list)
print(actor_rating_list)
print(movie_role_rating)





