# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:33:35 2018

@author: Mr.Minh
"""
from pymongo import MongoClient
import datetime
import dateutil.parser
import MySQLdb
import MySQLdb.cursors
import pymongo 
POST_COLLECTION = "posts"
POST_TABLE = "posts_view"
DT_FORMAT = '%Y-%m-%d %H:%M:%S'

def convertStrToDatetime(s):
    d = dateutil.parser.parse(s)
    return d

class Mungen(object):
    def __init__(self):
        self.toppick_uri = "mongodb://minhnt10:minh%40123@42.113.207.172:27017/admin"
        self.tp_client = MongoClient(self.toppick_uri)
        self.tp_db = self.tp_client['toppick'] 
        
    def get_all_post_token(self,condition = {},field = None):
        cursor = self.tp_db.posts.find(condition,field).sort([("_id", pymongo.ASCENDING)])
        return [item for item in cursor]
    
    def insert_many(self,collection,data):
        timestamp = datetime.datetime.now()
        for item in data:
            item['created_at'] = timestamp
        self.tp_db.get_collection(collection).insert_many(data)
    
    def update_one(self,collection,item_id,field,upsert=False):
        field['updated_at'] = datetime.datetime.now()
        self.tp_db.get_collection(collection).update_one({'_id': item_id}, {"$set": field}, upsert=upsert)

    def get_recommend(self, item_id):
        return self.tp_db.get_collection(POST_COLLECTION).find_one({"_id" : item_id},{"recommend" : 1})
    
    def post_count(self):
        return self.tp_db.get_collection(POST_COLLECTION).count_documents({})
    
class MuhExKillEl(object):
    
    def __init__(self):
        self.db = MySQLdb.connect(port=3306,
                    host="103.56.158.108",    # your host, usually localhost
                     user="wordpress_dev",         # your username
                     passwd="Topica@123",  # your password
                     db="wordpress_dev",
                     cursorclass=MySQLdb.cursors.DictCursor,charset='utf8')    
        
    def query(self,query,already_failed = False):
        try:
            cur = self.db.cursor()
            cur.execute(query)
        except:
            if already_failed:
                raise ValueError("Fail to reconnect MySQL!")
            self.__init__()
            return self.query(query,True)
        res = []
        for row in cur.fetchall():
            res.append(row)
        return res
    
    def get_new_post(self, days = 1, hours = 0):
        current = datetime.datetime.now()
        before = current - datetime.timedelta(days=days,hours=hours)
        before = before.strftime(DT_FORMAT)
        return self.query('select distinct id,post_content from {} where post_date >= \'{}\' order by id '.format(POST_TABLE,before))
        
    def get_post_conent(self,item_id):
        return self.query("select post_content from {} where id = {}".format(POST_TABLE,item_id))
    
    def get_all_post_content(self):
        return self.query("select distinct id,post_content from {} order by id".format(POST_TABLE))