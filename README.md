# Scenario_Rec
home page's Scenario Recommdation 
針對首頁的情境推薦 及  外匯推薦頁

### Structure
```
├─Demo3
│     ├──Rec
│           ├──Dockerfile             #dockerfile
│           ├──demo3_server_v1.py     #Recommend System
│           └──requirements.txt       #docker requirement
│     ├──unit_test
│           └──test.py                #unit_test
│
│     ├── Dockerfile                      #dockerfile
│     ├── Inser_json_DB.py                #tag server
│     ├── TAG_LOG_DOWNLOAD.xlsx           #tag data
│     ├── TAG_Value_DOWNLOAD.xlsx         #Tag data with value raw metadata
│     ├── getTags.py                      #load tag
│     ├── main_edition.json               #Seg1 data for offer 
│     ├── second_edition.json             #Seg2 data for offer
│     ├── tag_offer.json                  #offer with offer tag
│     └── requirements.txt       #docker requirements
│
│
├─test_api                           #stress test and unit test 
│     ├── 1_API_Scenario_Rec.docx    #API文件
│     ├── 2_測試文件                  #jmeter scipt for stress testing (azure)
│     ├── 3_服務目的                  #jmeter scipt for stress testing (gcp)
│     ├── Test_output.json           #test data for jmeter
│     ├── sample_submission.csv      #unit test
│     └── 壓力測試文件＿子慶.docx
│─readme.md                      #project descrpition 
└─docker-compose.yml             #docker-compose file
```






## 如何使用
```
docker-compose up --build
```

## 終止服務
```
docker-compose down
```

# unit test路徑
```
/Scenario_Rec/Demo3/unit_test/test.py
目前有unit_test只有針對已經起來的服務，所以使用時，需要調整url1這個變數
```

#
