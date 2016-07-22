#coding:utf-8
'''
Created on 2016��5��9��

@author: legnwei
'''

import json
import time
from dbcon import MyDB


def Return_keyvaluelist(handlelist=[]):
    resultlist=[]
    for k in handlelist:
        resultlist.append(k['name'])
    return resultlist
        

class PropHandler():
    def __init__(self,dbname='fish3'):
        self.__hdb=MyDB(dbname)
        self.__propfiles   =  json.load(file("config\\prop_FISH.json"), "utf-8")
        self.__proplist    =  self.__propfiles['props']
        
    def getdb(self):
        return self.__hdb
    
    def getproplist(self):
        return self.__proplist
    
    def changeproplist(self,filestr):
        self.__propfiles   =  json.load(file(filestr), "utf-8")
        self.__proplist    =  self.__propfiles['props']      
    
    def getpropvalue(self,propindex,key):
        return self.__proplist[propindex][key]
        
    def setpropvalue(self,propindex,key,propvalue):    
        self.__proplist[propindex][key]=propvalue
        
    def checkuid(self,uid):
        if uid!='':
            SQL_checkuid='SELECT uid from money where uid=%s'%(str(uid))
            resultuid=self.getdb().myfetchone(SQL_checkuid)
            if resultuid==None:
                return False
            else:
                return True
        else:
            return False
    
    def checkpropid(self,propid):
        propid =int(propid)
        if propid!='':
            for search in self.__proplist:
                if search['id']==propid:
                    break
            if search['id']==propid:
                return True
            else:
                return False
        else:
            return False

    def returnnametopropid(self,name):
        for search in self.__proplist:
            if search['name']==name:
                return search['id']
        return 0
            
    def returnvalidpropvalue(self,propid,propnum):
        if int(propid)<2000000:
            return int(propnum)
        else:
            return int(propnum)*86400
 
    def addallprops(self,uid,propnum):
        if self.checkuid(uid)==False:
            return False
        for kprop in range(len(self.__proplist)):
            temp_id=self.getpropvalue(kprop, 'id')
            if temp_id<2000000:
                self.setpropvalue(kprop, 'value', int(propnum))
            else:
                self.setpropvalue(kprop, 'value', int(time.time())+86400*30)
            SQL_check= 'SELECT id FROM prop WHERE uid=%s AND pid=%d'%(uid,temp_id)
            temp_value=self.getpropvalue(kprop, 'value')
            if self.getdb().myfetchone(SQL_check)==None:    
                SQL_add= 'INSERT INTO prop(uid,pid,pvalue) values (%s,%d,%d)'%(uid,temp_id,temp_value)
            else:
                SQL_add= 'UPDATE prop set pvalue=%d WHERE uid=%s and pid=%d'%(temp_value,uid,temp_id)
            self.getdb().myinsertorupdate(SQL_add)
        self.getdb().mycommit()
        self.getdb().myclose()
        return True

    def updateprops(self,uid,propid,propnum=1):
        if self.checkuid(uid)==False or self.checkpropid(propid)==False:
            return False
        SQL_isuidexist='SELECT id FROM prop WHERE uid=%s AND pid=%s'%(str(uid),str(propid))  
        result=self.getdb().myinsertorupdate(SQL_isuidexist)      
        if result!=0:
            SQL_update='UPDATE prop set pvalue=pvalue+%s WHERE uid=%s and pid=%s'%(str(self.returnvalidpropvalue(propid, propnum)),str(uid),str(propid))
        elif propid>=2000000:
            SQL_update='INSERT INTO prop(uid,pid,pvalue) values (%s,%s,%s)'%(str(uid),str(propid),str(self.returnvalidpropvalue(propid, propnum)+int(time.time())))
        else:
            SQL_update='INSERT INTO prop(uid,pid,pvalue) values (%s,%s,%s)'%(str(uid),str(propid),str(self.returnvalidpropvalue(propid, propnum)))            
        print SQL_update
        print SQL_isuidexist
        self.getdb().myinsertorupdate(SQL_update)      
        self.getdb().mycommit()
        self.getdb().myclose()
        return True
       
    def addmoneyanddiamond(self,uid,num,addtype): 
        if self.checkuid(uid)==False or num.isdigit()==False:
            return False
        if addtype ==0:
            addtype = 'money'
        elif addtype == 1:
            addtype = 'diamond'
        else :
            addtype=  'lottery'                
        SQL_ADD='UPDATE money SET %s=%s where uid=%s'%(addtype,str(num),str(uid))
        self.getdb().myinsertorupdate(SQL_ADD)  
        self.getdb().mycommit()
        self.getdb().myclose()
        return True
        

        
            
            
            
    
