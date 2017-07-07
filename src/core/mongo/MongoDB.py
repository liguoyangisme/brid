# -*- coding: utf-8 -*-
from pymongo import MongoClient

from core.utils import FileUtils

"""配置信息"""
config = FileUtils.readJSON("conf/config.json")

"""数据库名称"""
databaseName = config["mongo"]["database"]

"""获得连接"""
def getClient():
    return MongoClient(config["mongo"]["host"], int(config["mongo"]["port"]))

"""
Mongo操作
@do 处理方法 
    def fun(database):
    @database 数据库
"""
def handle(do):
    client = getClient()
    do(client[databaseName])
    client.close()

"""
Mongo 连接对象
"""
class MongoObject(object):

    """连接"""
    client = getClient()

    """数据库"""
    database = client[databaseName]

    """构造"""
    def __init__(self, table):

        """表"""
        self.table = self.database[table]

    """记录数量"""
    def count(self):
        return self.table.count()

    """查询"""
    def find(self, query):
        return self.table.find(query)

    """查询一条"""
    def findOne(self, query):
        return self.table.find_one(query)

    """插入"""
    def save(self, document):
        self.table.insert_one(document)

    """批量插入"""
    def saveBatch(self, documents):
        self.table.insert_many(documents)

    """更新"""
    def update(self, query, document):
        self.table.update_one(query,document)

    """更新多条"""
    def updateMany(self, query, document):
        self.table.update_many(query, document)

    """删除"""
    def delete(self,query):
        self.table.delete_many(query)

    """删除一条"""
    def deleteOne(self,query):
        self.table.delete_one(query)

    """关闭连接"""
    def close(self):
        self.client.close()

