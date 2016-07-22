#coding:utf-8
'''
Created on 2016/09/10

@author: lengwei
'''

from datatk.dbcon import MyDB

import codecs
import json

time1='00:00:00'
time2='23:59:59'

datelist=['2016-07-02','2016-07-03','2016-07-04']

itemdate=json.load(file('treasure_log.json'), 'utf-8')

def treasure_log(logdate,logtype="G"):
    db=MyDB('fish3')
    sqls1="SELECT DATE_FORMAT(time, '%Y-%m-%d') days,COUNT(DISTINCT (uid)) '抽奖人数',COUNT(uid) '抽奖次数',COUNT(uid) / COUNT(DISTINCT (uid)) '人均次数',SUM(IF(consume = 'G0', 1, 0)) '免费次数',SUM(IF(consume = 'G888', 1, 0)) '单抽次数(不含免费)',SUM(IF(consume = 'G8000', 1, 0)) '十连抽次数',SUM(IF(item = 'G', num, 0)) '产出金币',SUM(IF(item = 'D', num, 0)) '产出钻石',SUM(IF(item LIKE 'P1009%', num, 0)) '产出强化石',SUM(IF(item ='P1010001', num, 0)) '产出普通碎片',SUM(IF(item in('P1010010','P1010011'), num, 0)) '产出武器碎片',  SUM(IF(item LIKE 'P2008%', 1, 0)) '产出武器',SUM(IF(item LIKE 'P1003%', num, 0)) '产出宝盒' FROM fish3.treasure_log WHERE consume LIKE '"+logtype+"%' GROUP BY days;"
    sqls2='SELECT item FROM fish3.treasure_log where time between "%s %s" and "%s %s" and consume like "%s%%"'%(logdate,time1,logdate,time2,logtype)
    datatable=db.myfetchall(sqls2)
    itemrecord=dict()
    for vis in datatable:
        recorditems(itemrecord,vis[0])
    if itemdate.get(logtype)==None:
        itemdate[logtype]=dict()
    else:
        itemdate[logtype][logdate]=itemrecord
    db.myclose()
    

def recorditems(itemrecord,itemstr):
    items=itemstr.split(',')
    for vi in items:
        itemtag=vi[0]
        if itemtag=="G" or itemtag=="D" or itemtag=="L":
            try:
                itemnum=int(vi[1:])
            except:
                return 0
        elif itemtag=="P":
            vip=vi.split('-')
            itemtag=vip[0]
            try:
                itemnum=int(vip[1])
            except:
                return 0
            if vi[1]=="2":
                itemnum=1
        else:
            return 0            
        if itemrecord.get(itemtag)==None:
            itemrecord[itemtag]=itemnum
        else:
            itemrecord[itemtag]+=itemnum
                
                        
        