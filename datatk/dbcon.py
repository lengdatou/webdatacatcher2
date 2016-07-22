#coding:utf-8
'''
Created on 2016��3��5��

@author: lengwei
'''

import MySQLdb as DB
#import json


class MyDB():
    def __init__(self,dbname): 
        #self.k_dblist  =  json.load(file("config\\database.json"), "utf-8")['dblist']
        self.k_dblist  ={
                            "fish3"       :   [
                                                "192.168.1.100",
                                                "root",
                                                "1111",
                                                "fish3",
                                                3306
                                              ],
                             "fish3-dev"  :    [
                                                "192.168.1.100",
                                                "root",
                                                "1111",
                                                "fish3-dev",
                                                3306
                                            ],                    
                             "dianwan"  :    [
                                                "192.168.1.100",
                                                "root",
                                                "1111",
                                                "dianwan",
                                                3306
                                            ]
                         }
        self.__db=DB.Connection(self.k_dblist[dbname][0],
                                self.k_dblist[dbname][1],
                                self.k_dblist[dbname][2],
                                self.k_dblist[dbname][3],
                                self.k_dblist[dbname][4])
        self.__cur=None
        self.__defaultdbname=dbname
    
    def defaultdbname(self):
        return self.__defaultdbname
        
    def mychangedb(self,dbname):
        self.mycloseconnection()
        self.__db=DB.Connection(  self.k_dblist[dbname][0],
                                  self.k_dblist[dbname][1],
                                  self.k_dblist[dbname][2],
                                  self.k_dblist[dbname][3],
                                  self.k_dblist[dbname][4])
                 
    def mycursor(self):
        if self.__db==None:
            self.myreconnect()
        if self.__cur==None:
            self.__cur=self.__db.cursor() 
        return self.__cur
    
    def myclose(self):
        self.mycursor().close()
        self.__cur=None

    def myfetchone(self,SQLSS):
        self.mycursor().execute(SQLSS)
        return self.mycursor().fetchone() 

    def myfetchall(self,SQLSS):
        self.mycursor().execute(SQLSS)
        return self.mycursor().fetchall()     
    
    def myinsertorupdate(self,SQLSS):
        return self.mycursor().execute(SQLSS)
        
    def mycommit(self):
        self.__db.commit()
    
    def mycloseconnection(self):
        if self.__cur!=None:
            self.__cur.close()
            self.__cur=None
        if self.__db!=None:
            self.__db.close()
            self.__db=None
            
    def myreconnect(self):
        self.__db=DB.Connection(self.k_dblist[self.defaultdbname][0],
                                self.k_dblist[self.defaultdbname][1],
                                self.k_dblist[self.defaultdbname][2],
                                self.k_dblist[self.defaultdbname][3],
                                self.k_dblist[self.defaultdbname][4])
        