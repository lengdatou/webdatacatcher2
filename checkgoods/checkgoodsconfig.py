# -*- coding:utf-8 -*- 
'''
Created on 2016年3月2日

@author: RD04
'''

import json
import os
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#===============================================================================
# if __name__ == "__main__":
#     fishs=json.load(file('fish.json'), 'utf-8')
#     fishid={}
#     for f in fishs:
#         fishid[str(f['id'])]=0
#         
#     fishrefresh=json.load(file('refresh5.json'), 'utf-8')
#     for ref in fishrefresh:
#         reftimes=3600/ref["interval"]
#         randall=0
#         for item in ref['items']:
#             randall=randall+item['rand']
#         for item in ref['items']:
#             if item['type']=='single':
#                 fishid[str(item['fishid'])]=fishid[str(item['fishid'])]+item['rand']*reftimes/randall
# 
#     
#     for i in fishid.keys():
#         print i,fishid[i]
#===============================================================================
    
#===============================================================================
# if __name__ == "__main__":
#     goods=json.load(file('otherjson\\trade.json'), 'utf-8')
#     evegood = goods['common2']
#     for f in evegood:
#         #print 'goodsId is',f['goodsId']
#         a=(f['cv']/5)/f['money']
#         b=(f['cvpool']/5)/f['money']
#         if a==300 and b==30:
#             print f['vis'],'||||',f['name'],f['money'],a,b,'OK'
#         else:
#             print 'error!!!!',f['vis'],'||||',f['name'],f['money'],a,b
#         print '------------------------------------'
#     raw_input()
#===============================================================================
 
partner  =  0
jsonname = 'goods'


VALUE_ITEM_TAG_GOLD             = u'G'
VALUE_ITEM_TAG_LOTTERY          = u'L'
VALUE_ITEM_TAG_PROP             = u'P'
VALUE_ITEM_TAG_DIAMOND          = u'D'


def printlist(listA,ifnewline=False):
    for i in listA:
        if ifnewline==False:
            print i,
        else:
            print i

def checklistinlist(listA,listB,specialnumlist=[37]):
    for i in listA:
        if i not in listB:
            if i in specialnumlist:
                continue
            else:
                return False
    return True

def getfiles(vname):
    allfiles=os.listdir('otherjson')
    tempfiles=[]
    for i in range(len(allfiles)):
        if allfiles[i].endswith(vname+'.json')==True:
                tempfiles.append(allfiles[i])
    return tempfiles
 
def checkgoods(vjsonname):
    goods=json.load(file('otherjson\\'+vjsonname), 'utf-8')
    paytypefile=json.load(file('otherjson\\'+'paytypelist.json'), 'utf-8')
    vpartner=vjsonname.split('-')[0]
    if vpartner==vjsonname or vpartner=='11':
        cvrate=300
        cvpoolrate=30
        vpartner='11'
    else:
        cvrate=150
        cvpoolrate=15
    if vjsonname.endswith('goods.json')==True:
        evegood = goods['goods']  
    else:
        evegood = goods['common2']
    countright=0
    countwrong=0
    for f in evegood:
        #print 'goodsId is',f['goodsId']
        a=(f['cv']/5)/f['money']
        b=(f['cvpool']/5)/f['money']
       # if f.get()
        if a==cvrate and b==cvpoolrate and (f['id']/1000-int(vpartner))==1000 and checklistinlist(f['paytypelist'], paytypefile[str(vpartner)]['paytypelist']):
            countright+=1
            ifeeror='Ok'
        else:
            countwrong+=1
            ifeeror='Error!!!!!'
        printobj=[f['paytypelist'],f['id'],'||||',f['vis'],'||||',f['name'],f['money'],a,b,ifeeror]
        printlist(printobj)
        print '\n------------------------------------'
    print "right : ",countright,", wrong : ",countwrong
    if countwrong>0:
        return paytypefile[vpartner]['name'],False
    else:
        return paytypefile[vpartner]['name'],True

            
def updateactions():
    filename='actions'
    allfiles=os.listdir('otherjson')
    tempfiles=[]
    for i in range(len(allfiles)):
        if allfiles[i].endswith(filename+'.json')==True:
                tempfiles.append(allfiles[i])
    for j in tempfiles:
        actionfile=json.load(file('otherjson\\'+j), 'utf-8')


def runcheckgoods():
    wrongfiles=[]
    if partner!=0:
        handlefilenames=[str(partner)+'-goods.json']
    else:
        handlefilenames=getfiles('goods')
    for vf in handlefilenames:
        checkresult=eval('checkgoods')(vf)
        if checkresult[1]==False:
            wrongfiles.append(checkresult[0])
    print 'Wrong files list is : ',json.dumps(wrongfiles,ensure_ascii=False,indent=4)
    
def getpaytypelist():
    handlefilenames=getfiles('trade')
    plist={}
    for vf in handlefilenames:
        vpartner=vf.split('-')[0]
        if vpartner==vf:
            vpartner='11'
        paytype=json.load(file('otherjson\\'+vf), 'utf-8')
        plist[vpartner]=paytype['common2'][0]['paytypelist']
    return plist

def parseValueItems(vstr):
    ret = []
    if len(vstr)==0:
        return ret
    strs = vstr.split(u',')
    for vs in strs:
        tag = vs[0]
        vstrs = vs[1:].split(u'-')
        
        vi = ValueItem()
        vi.type = VALUE_ITEM_TAG_MAP.get(tag)
        for sss in vstrs:
            vi.values.append(int(sss))
        ret.append(vi)
        if vi.type==const.VALUE_ITEM_TYPE_PROP:
            assert len(vi.values)==2#道具类型,[id,count]
    return ret

def valueItemList2String(vilist):
    ret = u''
    for vi in vilist:
        ret += (vi.toString() + u',')
    if len(ret)==0:
        return ret
    return ret[:-1]

def makeValueItemString(gold, lottery, propid, propcount):
    ret = u''
    if gold>0:
        ret += (u'%s%d,' % (const.VALUE_ITEM_TAG_GOLD, gold))
    if lottery>0:
        ret += (u'%s%d,' % (const.VALUE_ITEM_TAG_LOTTERY, lottery))
    if propid>0:
        ret += (u'%s%d-%d,' % (const.VALUE_ITEM_TAG_PROP, propid, propcount))
    if len(ret)==0:
        return ret
    return ret[:-1]


def qudao():
    a=[[11,u"官网"]    ,
        [13,u"百度推广"]    ,
        [16,u"appstore"]    ,
        [17,u"91助手"]    ,
        [18,u"itools"]    ,
        [19,u"360渠道"]    ,
        [22,u"小米"]    ,
        [23,u"豌豆荚"]    ,
        [24,"快用"]    ,
        [33,"oppo"]    ,
        [36,"应用汇"]    ,
        [40,"酷派"]    ,
        [41,"华为"]    ,
        [42,"安智"]    ,
        [46,"xy"]    ,
        [49,"vivo"]    ,
        [50,u"卓悠"]    ,
        [51,"百度手机助手"]    ,
        [67,"酷狗"]    ,
        [71,"应用宝"]    ,
        [72,"咪咕"]    ,
        [75,"同步推"]    ,
        [76,"联想单机"]    ,
        [77,"金立单机"]    ,
        [78,"安卓APP"]    ,
        [79,"微信QQ分享"]    ,
        [80,"草花"]    ,
        [82,"虫虫"]    ,
        [83,"优亿"]    ,
        [84,"木蚂蚁"]    ,
        [85,"百度(2)"]    ,
        [86,"7k7k"]    ,
        [87,"HTC"]    ,
        [91,"松果"]    ,
        [92,"咪咕官方"]    ,
        [93,"360(2)"]    ,
        [94,"应用宝(2)"]    ,
        [95,"小米(2)"]    ,
        [96,"联想(2)"]    ,
        [97,"appstore大玩家"]    ,
        [98,"oppo(2)"]    ,
        [100,"酷派(2)"]    ,
        [101,"华为(2)"]    ,
        [102,"百度单机(2)"]    ,
        [103,"appstore(3)"]    ,
        [104,"台湾联运"]    ,
        [105,"欢乐捕鱼OL"]    ,
        [106,"疯狂捕鱼OL"]    ,
        [107,"深海捕鱼OL"]    ,
        [108,"全民捕鱼OL"]    ,
        [109,"捕鱼大冒险OL"]    ,
        [110,"捕鱼OL"]    ,
        [111,"超级捕鱼"]    ,
        [114,"捕鱼经典版"]    
        ]
    b={
            "93": [51],
            "51": [29],
            "67": [33],
            "98": [56],
            "50": [27],
            "91": [47],
            "88": [47],
            "89": [47],
            "111": [69],
            "110": [68],
            "113": [70],
            "112": [37],
            "82": [46],
            "83": [47],
            "80": [44],
            "81": [45],
            "86": [47],
            "87": [47],
            "84": [47],
            "85": [50],
            "24": [12],
            "92": [37],
            "22": [10],
            "23": [11],
            "46": [25],
            "95": [53],
            "42": [22],
            "40": [20],
            "41": [21],
            "96": [54],
            "75": [38],
            "77": [43],
            "76": [41,37],
            "108": [66],
            "109": [67],
            "72": [37],
            "71": [34],
            "102": [59],
            "103": [60],
            "100": [57],
            "101": [58],
            "106": [64],
            "107": [65],
            "97": [55],
            "105": [63],
            "11": [1,28,39,37,2],
            "99": [47],
            "17": [4],
            "16": [5],
            "19": [7,37],
            "18": [6],
            "49": [40,37],
            "37": [18],
            "36": [42],
            "33": [17],
            "94": [],
            "114":[71]
        }
    
    c=dict()
    for i in a:
        c[str(i[0])]=dict()
        c[str(i[0])]['name']=i[1]
        try:
            c[str(i[0])]['paytypelist']=b[str(i[0])]
        except:
            c[str(i[0])]['paytypelist']=b['11']
    filejson=codecs.open('otherjson\\paytypelist.json',"w+","utf-8")
    obj_formated = json.dumps(c,ensure_ascii=False,indent=4)
    filejson.write(obj_formated)
    filejson.close()    
    print obj_formated    

    
                
   
