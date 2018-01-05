
# coding: utf-8

# In[14]:




import pandas as pd
import json
from datetime import datetime
import calendar 
from flask import Flask
from flask import jsonify
import redis
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import inspect, os
import psycopg2
import math


redis_ip = 'liaofxredis'
r = redis.Redis(host=redis_ip,port=6379,db=0)
#db connect

#r = redis.Redis(host='localhost',port=6379,db=0)
HOST = "liaofxpostgres"
USER = 'postgres'
PASSWORD = 'demois1207'
DB = 'postgres'
sql_conn = psycopg2.connect(database = DB,
                        host = HOST,
                        user = USER,
                        password = PASSWORD)
cur = sql_conn.cursor()


# In[3]:

a = inspect.getfile(inspect.currentframe())
b = os.path.dirname(os.path.abspath(a)) 
file_path_main_edition = os.path.join( b , 'main_edition.json' )
jsonfile = open(file_path_main_edition,'r')
main_Json = json.load(jsonfile)
file_path_second_edition = os.path.join( b , 'second_edition.json' )
jsonfile = open(file_path_second_edition,'r')
second_Json = json.load(jsonfile)
file_path_TagDB = os.path.join( b , 'TAG_DB.json' )
jsonfile = open(file_path_TagDB,'r')
TagDB_Json = json.load(jsonfile)
file_path_tag_offer = os.path.join( b , 'tag_offer.json' )
jsonfile = open(file_path_tag_offer,'r')
TagOffer_Json = json.load(jsonfile)


# In[4]:

SQL= 'CREATE TABLE main_edition ( id serial NOT NULL PRIMARY KEY , tag_info json NOT NULL )'
cur.execute(SQL)
sql_conn.commit()


# In[4]:

SQL= 'CREATE TABLE second_edition ( id serial NOT NULL PRIMARY KEY , tag_info json NOT NULL )'
cur.execute(SQL)
sql_conn.commit()


# In[5]:

SQL= 'CREATE TABLE tag_db ( id serial NOT NULL PRIMARY KEY , tag_info json NOT NULL )'
cur.execute(SQL)
sql_conn.commit()


# In[6]:

SQL= 'CREATE TABLE offer_tagging ( id serial NOT NULL PRIMARY KEY , off_info json NOT NULL )'
cur.execute(SQL)
sql_conn.commit()


# In[6]:

for i in main_Json:
    SQL = "INSERT INTO main_edition(tag_info) VALUES('{}');".format(json.dumps(i))
    cur.execute(SQL)
    sql_conn.commit()


# In[7]:

for i in second_Json:
    SQL = "INSERT INTO second_edition(tag_info) VALUES('{}');".format(json.dumps(i))
    cur.execute(SQL)
    sql_conn.commit()


# In[8]:

for i in TagDB_Json:
    SQL = "INSERT INTO tag_db(tag_info) VALUES('{}');".format(json.dumps(i))
    cur.execute(SQL)
    sql_conn.commit()


# In[9]:

for i in TagOffer_Json:
    SQL = "INSERT INTO offer_tagging(off_info) VALUES('{}');".format(json.dumps(i))
    cur.execute(SQL)
    sql_conn.commit()


# In[12]:

# 貼標庫格式
def Tag_query(tag, sql_db):
    SQL = "SELECT tag_info FROM tag_db WHERE tag_info->>'TAG_ID' = '{}';".format(tag)
    sql_db.execute(SQL)
    records = sql_db.fetchall()[0][0]
    data = {}
    data['TAG_ID'] = records['TAG_ID']
    data['scenario'] = records['scenario']
    data['dataSource'] = records['dataSource']
    data['securityFilter'] = records['securityFilter']
    data['tagTime'] = time.time()
    data['expireTime'] = time.time() + records['expireAfter']
    data['isValid'] = records['isActive']
    return data


# In[11]:

SQL= "Select tag_info from tag_db  where tag_info ->>'TAG_ID' = 'TG0001';"
cur.execute(SQL)
cur.fetchall()


# In[16]:

file_path = inspect.getfile(inspect.currentframe())
file_direction = os.path.dirname(os.path.abspath(file_path))
tagging_log = os.path.join( file_direction , 'TAG_LOG_DOWNLOAD.xlsx' )
tagging_value_log = os.path.join( file_direction , 'TAG_Value_DOWNLOAD.xlsx' )
df = pd.read_excel(tagging_log)
df_value = pd.read_excel(tagging_value_log)


# In[18]:

def TaggingDB_ETL(data,data_value, TagDB=cur, TaggingDB=r):
    vids = data.ID.unique()
    for i in vids:
        Tagging = {}
        Tagging['VID'] = i
        Tagging['batchTag'] = []
        Tagging['realtimeTag'] = []
        tag = data[data.ID==i]['UTID']
        tag_value = data_value[data_value.ID == i]['UTID']
        for j in tag:
            Tagging['batchTag'].append(Tag_query(j, TagDB))
        for j in tag_value:
            tag_data = Tag_query(j, TagDB)
            tag_data['Tag_Value'] = (data_value[(data_value.ID == i) & (data_value.UTID==j)]['TAG_VALUE'].values[0])
            Tagging['batchTag'].append(tag_data)
        TaggingDB.set(i, json.dumps(Tagging,ensure_ascii=False))


# In[20]:

TaggingDB_ETL(df,df_value,TagDB=cur,TaggingDB=r)

