# coding: utf-8

# In[ ]:




# In[ ]:


import pandas as pd
import json
from datetime import datetime
import calendar 
from flask import Flask,g
from flask import jsonify
from flask import request
import redis
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import inspect, os
import psycopg2
import math
#version1.1 add CB
#import pybreaker

#time_breaker = pybreaker.CircuitBreaker(fail_max=3,reset_timeout=30)

#end default user tag
    



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
redis_ip = 'liaofxredis'
#r = redis.Redis(host=redis_ip,port=6379,db=0)
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
#r = redis.Redis(host='localhost',port=6379,db=0,socket_timeout=0.1)
#sql_conn = psycopg2.connect(database = "MJ_PROTOTYPE",
#                        host = "localhost",
#                        user = "liaoziqing",
#                        password = "")


cur = sql_conn.cursor()
@app.route('/')
def hello():
  return "HI"

# 取得目前所有使用者名單

@app.route('/user/Scenario_Rec',methods=['GET'])
def getUserScenarioRec():
#  label = json.loads(db[db.UID == uid].to_json(orient='records',force_ascii=False))
    vid = request.args.get('vid')
    try:
        label = get_second_offer(int(vid))
    except:
        label = {
      "Offer": ["OFF0039", "OFF0035", "OFF0036", "OFF0037", "OFF0038", "OFF0042", "OFF0062"], 
      "Offer1": ["OFF0010", "OFF0021", "OFF0045", "OFF0008", "OFF0001", "OFF0005", "OFF0011", "OFF0013", "OFF0015", "OFF0020"], 
      "offer_desc": "想成家的您絕對不能錯過", 
      "offer_desc1": "旅遊大小事報你知透透"
        }
    res = jsonify(label)
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    return res

@app.route('/user/FX_Rec',methods=['GET'])
def getUserFXRec():
#  label = json.loads(db[db.UID == uid].to_json(orient='records',force_ascii=False))
    vid = request.args.get('vid')
    try:
        label = get_fx_rec(int(vid))
    except:
        label = {
      "Offer": ["OFF0063"], 
      "Offer1": ["OFF0026", "OFF0027", "OFF0022", "OFF0024", "OFF0028", "OFF0023", "OFF0025"]
        }
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
    offer_set12 = {}
    offer_set12['Offer'] = offer1
    offer_set12['Offer1'] = [t[0] for t in offer_output]
    return offer_set12

def get_user_tag(user_id):
    r_get = r.get(user_id)
    if r_get !=None :
        user_get = json.loads(r_get)
    else:
        default_value = 1
        user_get = json.loads(r.get(default_value))
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
    #
    get_rec_offer = getSeg_ref('second_edition',Tag_Value,cur)
    #
    rec_offer = get_rec_offer['offer_list']
    rec_offer1= get_rec_offer['offer_list1']
    #rec_offer = getSeg_ref('second_edition',Tag_Value,cur)['offer_list']
    #rec_offer1= getSeg_ref('second_edition',Tag_Value,cur)['offer_list1']
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
    offer_set12['offer_desc'] = get_rec_offer[u'offer_desc']
    offer_set12['Offer1'] = offer_list1
    offer_set12['offer_desc1'] = get_rec_offer[u'offer_desc1']
    return offer_set12

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)


