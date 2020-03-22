# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/18 11:33
# @IDE:         PyCharm

import redis

HOST = 'localhost'
PORT = '6379'
PASSWORD = '123waq'

r_db = redis.Redis(host=HOST,
                   port=PORT,
                   password=PASSWORD,
                   decode_responses=True,   # decode_responses=True，写入value中为str类型，否则为字节型
                   db='0')                  # 默认不写是db0

# r_db.hset("30391241","name","切尔诺贝利·禁区电影版")
print(type(r_db.hget("movie_detail",3039124)))
# set的几个参数：
'''
前面两个，一个key，一个value
ex，过期时间（秒）
px，过期时间（毫秒）
nx，如果设置为True，则只有name不存在时，当前set操作才执行
xx，如果设置为True，则只有name存在时，当前set操作才执行
'''

# print(r_db['name'])
# print(r_db.get('name'))
# print(type(r_db.get('name')))