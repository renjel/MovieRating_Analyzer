# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/17 14:48
# @IDE:         PyCharm
import datetime
from time import sleep

import requests
import json



# 添加请求头
from Mysql_conn.mysql_run import db_conn

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Cookie" : '__vwo_uuid_v2=DF1CD1D02C1F8E768DBF47BF79A9F1E74|b12b5befc6df7585392eb4a002c4cf90; douban-fav-remind=1; __gads=ID=3eea0cf197f18381:T=1572193084:S=ALNI_MZEvinttZ6YoG1H45Vo0sCZPtiCXw; ll="118201"; bid=llzh4k6OdTQ; __yadk_uid=E1wIZqTUqiTVorlunoLDtHi9gdAb1vcO; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21387; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1584629576%2C%22http%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DEcbe2nvJJLpO89mnKeeZdj2E0gA1uItjZfbFCQRXIyG6BqAvcd1PZCoVXx_jdzjC%26wd%3D%26eqid%3Db4b20890000a8e5b000000065e738746%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1436318017.1543845487.1584549796.1584629577.16; __utmc=30149280; __utmz=30149280.1584629577.16.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; ap_v=0,6.0; dbcl2="213873128:4KaTmtgwOO8"; ck=AuFd; _pk_id.100001.8cb4=06fcdbfb123571fb.1551262554.7.1584629702.1584549794.; __utmb=30149280.3.10.1584629577'
}

headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}
url_tag = "https://movie.douban.com/j/search_tags?type=movie"

tags = json.loads(requests.get(url_tag,headers=headers).text)["tags"]

print(tags)
print(type(tags))

movie_info = {}
stat = 0
for tag in tags:
    if tag == "可播放":
        continue
    movie_tag_info = {}
    # i = 0
    # j = 1

    # while True:
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=" + tag + "&sort=time&page_limit=1000&page_start=0"
    # print(url)
    try:
        if stat == 0:
            tag_info = json.loads(requests.get(url, headers=headers).text)
            stat = 1
        else:
            tag_info = json.loads(requests.get(url, headers=headers2).text)
            stat = 0
    except Exception as e1:
        print(e1)
        break
    for tag_movie in tag_info["subjects"]:
        movie = {"title":tag_movie["title"],"url":tag_movie["url"],"playable":tag_movie["playable"],"rate":tag_movie["rate"]}
        movie_tag_info[tag_movie["id"]] = movie
    # i += 1
    # j += 1
    # if j > 100:
    #     break
    sleep(10)
    movie_info[tag] = movie_tag_info
    print(datetime.datetime.now().strftime("%Y--%m--%d %H:%M:%S") + "." + str(datetime.datetime.now().microsecond)[0:3])
    print("tag:" + tag + " is complete, count:" + str(len(list(movie_tag_info.keys()))))
    # break

# print(json.dumps(movie_info))

# 初始化数据库连接
db = db_conn("renjel", "123waq", "Movie_analyzer")
db.test()
# 数据库插入值
insertVal = ""
# 把电影内容插入数据表
i = 0
total = 0
for tag in movie_info:
    id_list_new = []
    id_list = db.select("distinct id", "movie_index", "")
    for id0 in id_list:
        id_list_new.append(id0[0])
    # print(id_list_new)
    for movie_id in movie_info[tag]:
        # print(movie_id)
        if int(movie_id) in id_list_new:
            # print(movie_id)
            continue
        else:
            total += 1
            insertVal = "" + movie_id + ",'" + movie_info[tag][movie_id]["title"] + "','" + movie_info[tag][movie_id]["url"] + \
                        "','" + str(movie_info[tag][movie_id]["playable"]) + "','" + movie_info[tag][movie_id]["rate"] + "','" + tag + "'"
            stats = db.insert("movie_index", insertVal)
            if stats == "OK":
                i += 1
            else:
                print("插入错误！本行数据为： (" + insertVal + ")")
            # print("当前插入到第 " + str(i) + " 行，本行数据为： (" + insertVal + ")")
db.stop_conn()
print("Total: " + str(total))
print("OK: " + str(i))


