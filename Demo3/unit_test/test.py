# encoding: utf-8


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest
import pandas as pd
import json
import datetime
import calendar 
from flask import Flask
from flask import jsonify
import inspect, os
#import get_Tag
import requests
import urllib



class CalculatorTestCase(unittest.TestCase):
   
    def setUp(self):
        pass
    #first run 
    def tearDown(self):
        pass
    
    #all named add test_
    def test_basic(self):
        self.assertEqual(1, 1)


    #def test_SamePathGetData(self):
    #    self.assertIsNotNone(get_Tag.SamePathGetData('Tagging_Db.xlsx'))
    #    self.assertIsNotNone(get_Tag.SamePathGetData('Tag_Db.xlsx'))
    
    def test_getScenarioDefault(self):
        default_label = {
      "Offer": ["OFF0039", "OFF0035", "OFF0036", "OFF0037", "OFF0038", "OFF0042", "OFF0062"], 
      "Offer1": ["OFF0010", "OFF0021", "OFF0045", "OFF0008", "OFF0001", "OFF0005", "OFF0011", "OFF0013", "OFF0015", "OFF0020"], 
      "offer_desc": u"想成家的您絕對不能錯過", 
      "offer_desc1": u"旅遊大小事報你知透透"
        }
        url1='http://ec2-18-217-99-39.us-east-2.compute.amazonaws.com:'
        url2='3010/user/Scenario_Rec?vid=5000'
        r=requests.get(url1+url2).json()
        self.assertEqual(default_label,r)
        
    def test_getScenario(self):
        default_label = {
      "Offer": ["OFF0050", "OFF0051", "OFF0052", "OFF0016", "OFF0054", "OFF0057"], 
      "Offer1": ["OFF0047", "OFF0049", "OFF0048", "OFF0012", "OFF0014", "OFF0055"], 
      "offer_desc": "晶饌美宴盡在玉山", 
      "offer_desc1": "卡利For你呀！即買即享即刻出發！"
        }
        url1='http://ec2-18-217-99-39.us-east-2.compute.amazonaws.com:'
        url2='3010/user/Scenario_Rec?vid=3'
        r=requests.get(url1+url2).json()
        self.assertEqual(default_label,r)
        
        
        
    def test_getFXDefault(self):
        default_label = {
      "Offer": ["OFF0063"], 
      "Offer1": ["OFF0026", "OFF0027", "OFF0022", "OFF0024", "OFF0028", "OFF0023", "OFF0025"]
        }
        url1='http://ec2-18-217-99-39.us-east-2.compute.amazonaws.com:'
        url2='3010/user/FX_Rec?vid=5000'
        r = requests.get(url1+url2).json()
        self.assertEqual(default_label,r)
        
    def test_getFX(self):
        default_label = {
      "Offer": ["OFF0021"], 
      "Offer1": ["OFF0026", "OFF0027", "OFF0022", "OFF0024", "OFF0028", "OFF0023", "OFF0025"]
        }
        url1='http://ec2-18-217-99-39.us-east-2.compute.amazonaws.com:'
        url2='3010/user/FX_Rec?vid=2'
        r = requests.get(url1+url2).json()
        self.assertEqual(default_label,r)
        # want to check add_fun
def add(a,b):
    return a+b







if __name__ == "__main__":
    unittest.main(verbosity=2)

