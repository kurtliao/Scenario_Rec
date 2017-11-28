# coding: utf-8

# In[ ]:




# In[ ]:


import pandas as pd
import json
from datetime import datetime
import calendar 
from flask import Flask
from flask import jsonify
import redis
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import inspect, os
import psycopg2
import math


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


redis_ip = 'fx_redis'
r = redis.Redis(host=redis_ip,port=6379,db=0)
#db connect

#r = redis.Redis(host='localhost',port=6379,db=0)
HOST = "fx_postgres"
USER = 'postgres'
PASSWORD = 'demois1207'
DB = 'postgres'
sql_conn = psycopg2.connect(database = DB,
                        host = HOST,
                        user = USER,
                        password = PASSWORD)

cur = sql_conn.cursor()
@app.route('/')
def hello():
  return "HI"

# 取得目前所有使用者名單

@app.route('/user/Scenario_Rec/<string:vid>',methods=['GET'])
def getUserScenarioRec(vid):
#  label = json.loads(db[db.UID == uid].to_json(orient='records',force_ascii=False))
  label = get_second_offer(int(vid))
  res = jsonify(label)
  res.headers['Content-Type'] = 'application/json; charset=utf-8'
  return res

@app.route('/user/FX_Rec/<string:vid>',methods=['GET'])
def getUserFXRec(vid):
#  label = json.loads(db[db.UID == uid].to_json(orient='records',force_ascii=False))
  label = get_fx_rec(int(vid))
  res = jsonify(label)
  res.headers['Content-Type'] = 'application/json; charset=utf-8'
  return res


def get_fx_rec(vid):
    user_tag=get_user_tag(vid)
    temp_batch=user_tag['batchTag']
    tag_list = [ t['TAG_ID'] for t in temp_batch if t[u'TAG_ID'] is not None]
    #business rule 
    if 'SEG001' in tag_list : 
        Tag_Value= [ t for t in temp_batch if t[u'TAG_ID'] =='SEG001'][0]['Tag_Value']
        if Tag_Value == 1:
            offer1 = [u'OFF0063']
        elif Tag_Value ==2:
            offer1 = [u'OFF0021']
        else:
            offer1 = [u'OFF0004']    
    else :
        Tag_Value = []
        offer1 = [u'OFF0004']
        #model rule
    fx_pag_tag = ['TG0001','TG0005','TG0109','TG0119','TG0114','TG0013','TG0110']
    fx_order = [u'OFF0022',u'OFF0023',u'OFF0024',u'OFF0025',u'OFF0026',u'OFF0027',u'OFF0028']
    offer_output = []
    for order in fx_order : 
        temp_ref = getoff_ref('offer_tagging',order,cur)['OFFER_TAG']
        offer_output.append ((order, max(get_inn_len(fx_pag_tag,temp_ref),get_inn_len(tag_list,temp_ref))))
    offer_output = sorted(offer_output, key=lambda ratio: ratio[1],reverse=True)
    offer_list =offer1 + [t[0] for t in offer_output]
    return offer_list

def get_user_tag(user_id):
    user_get = json.loads(r.get(user_id))
    return user_get
def getSeg_ref(table,tag_value,sql_db):
    SQL = "Select tag_info from " + table + " where tag_info ->> 'Tag_Value' = '{}'".format(tag_value)
    cur.execute(SQL)
    records = cur.fetchall()[0][0]
    return records
def getoff_ref(table,tag_value,sql_db):
    SQL = "Select off_info from " + table + " where off_info ->> 'OFFER_ID' = '{}'".format(tag_value)
    cur.execute(SQL)
    records = cur.fetchall()[0][0]
    return records
def get_tag_cos(TL1,TL2):
    return (len([t for t in TL1 if t in TL2])/math.sqrt(len(TL1)*len(TL2)))
def get_inn_len(TL1,TL2):
    return (len([t for t in TL1 if t in TL2]))

def get_second_offer(vid):
    describe = '大版位的情境推薦'
    user_tag = get_user_tag(vid)
    temp_batch = user_tag['batchTag']
    tag_list = [ t['TAG_ID'] for t in temp_batch if t[u'TAG_ID'] is not None]
    Tag_Value = [ t for t in temp_batch if t[u'TAG_ID'] =='SEG002'][0]['Tag_Value']
    rec_offer = getSeg_ref('second_edition',Tag_Value,cur)['offer_list']
    rec_offer1= getSeg_ref('second_edition',Tag_Value,cur)['offer_list1']
    offer_output = []
    for offer in rec_offer:
        offer_output.append((offer, get_tag_cos(tag_list,getoff_ref('offer_tagging',offer,cur)['OFFER_TAG']) ))
    offer_output = sorted(offer_output, key = lambda ratio : ratio[1], reverse = True)
    offer_list = [t[0] for t in offer_output]
    offer_output1 = []
    for offer in rec_offer1:
        offer_output1.append((offer, get_tag_cos(tag_list,getoff_ref('offer_tagging',offer,cur)['OFFER_TAG']) ))
    offer_output1 = sorted(offer_output1, key = lambda ratio : ratio[1], reverse = True)
    offer_list1 = [t[0] for t in offer_output1]
    offer_set12 = {}
    offer_set12['Offer'] = offer_list
    offer_set12['Offer1'] = offer_list1
    return offer_set12

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)


