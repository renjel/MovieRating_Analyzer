# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Site: 
# @File: mysql_run.py
# @Author: Renjel
# @E-mail: renjel@foxmail.com
# @Time: 2月 15, 2020
# ---

import pymysql

class db_conn():

    def __init__(self, username, password, database):
        # self.username = username
        # self.password = password
        # self.database = database
        # 打开数据库连接
        self.db = pymysql.connect("localhost", username, password, database)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    def test(self):
        # 使用 execute()  方法执行 SQL 查询
        self.cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取单条数据
        data = self.cursor.fetchone()
        print("Database version : %s " % data)

    def stop_conn(self):
        # 关闭数据库连接
        self.db.close()

    def insert(self,table,insertVal):
        # SQL 插入语句
        sql = "INSERT INTO %s VALUES (%s)" % (table, insertVal)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
            return "OK"
        except:
            # 发生错误时回滚
            self.db.rollback()
            return "ERROR"

    def select(self,selectVal,table,condition):
        sql = "select %s from %s %s" % (selectVal,table,condition)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")
            return "ERROR"




