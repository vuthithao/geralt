# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 15:37:33 2018

@author: MinhNguyen
"""
import service
import MySQLdb
import MySQLdb.cursors
import datetime
import graypy
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = graypy.GELFHandler(service.GRAY_LOG_URL, 5555)
logger.addHandler(handler)
DT_FORMAT = '%Y-%m-%d %H:%M:%S'
db = MySQLdb.connect(port=3306,
                    host="103.56.158.108",    # your host, usually localhost
                     user="wordpress_dev",         # your username
                     passwd="Topica@123",  # your password
                     db="wordpress_dev",
                     cursorclass=MySQLdb.cursors.DictCursor,charset='utf8')    
print("Start crawling...")
cur = db.cursor()
current = datetime.datetime.now()
before = current - datetime.timedelta(minutes = 30)
before = before.strftime(DT_FORMAT)
cur.execute('select * from wordpress_dev.wp_has_read where read_post_time >= \'{}\''.format(before))
cnt = 0
for row in cur.fetchall():
    cnt += 1
    row['read_post_time'] = row['read_post_time'].isoformat(' ')
    logger.info({"type" : "mysql_record","data" : str(row)})
db.close()
print("Successful crawled {} item from {} to {}".format(cnt,before,current.strftime(DT_FORMAT)))


