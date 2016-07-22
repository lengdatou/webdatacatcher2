# -*- coding:utf-8 -*- 
'''
Created on 2016/07/10
中文会乱码？！！？？？

@author: lengwei
'''

import urllib,urllib2,cookielib
import json
from bs4 import BeautifulSoup
from checkgoods import printlist
from string import strip
import openpyxl
from dataforexcel import textlistformated
from datetime import date,timedelta



class MyDataCatcher():
    def __init__(self):
        self.__innerjson=json.load(file('config\\urldata.json'),'utf-8')
        self.__dataurl=self.__innerjson.get('dataurl')
        self.__datebegin=self.__innerjson.get('date').get('begin')
        self.__dateend=str(date.today()-timedelta(1))
        self.__lastfile=self.__innerjson.get('date').get('lastfile')
        
    def getcontent(self,sendurlbefore):
        return urllib2.urlopen(self.makeurl(sendurlbefore)).read()
    
    def makeurl(self,sendurlbefore):
        url  =sendurlbefore
        begin=self.__datebegin
        end  =self.__dateend
        combinstr=url+'&begdate='+begin+'&enddate='+end
        return combinstr
    
    def evaluatelogin(self):
        #登录的主页面  
        hosturl = self.__innerjson.get('hosturl')
        #post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
        posturl = self.__innerjson.get('posturl') 
          
        #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
        cj = cookielib.LWPCookieJar()  
        cookie_support = urllib2.HTTPCookieProcessor(cj)  
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
        urllib2.install_opener(opener)  
          
        #打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
        urllib2.urlopen(hosturl)  
          
        #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
        headers  = self.__innerjson.get('headers')
        #构造Post数据，他也是从抓大的包里分析得出的。  
        postData = self.__innerjson.get('postData')  
          
        #需要给Post数据编码  
        postData = urllib.urlencode(postData)  
          
        #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
        request = urllib2.Request(posturl, postData, headers)
        urllib2.urlopen(request)  
 
    def getdatatable(self,datatable):
        names=list()
        data=list()
        tt=datatable
        for mm in tt.thead.tr:
            if strip(str(mm.string)) not in ['','\n','None']:
                names.append(strip(str(mm.string)))
        for nn in tt.tbody.children:
            try:
                templist=list()
                for qq in nn:
                    if strip(str(qq.string)) not in ['','\n','None']:
                        templist.append(strip(str(qq.string)))
                data.append(templist)
            except:
                continue
        printlist(names)
        print '\r'
        for i in data:
            printlist(i)
            print '\r'
        return names,data
 
    def beautifulsouphtml(self,htmlcontent=''):   
        soup = BeautifulSoup(htmlcontent) 
        return self.getdatatable(soup.find(id='datatable'))
    
    def beautifulsouphtmlmultiple(self,htmlcontent='',fortimes=1):   
        soup = BeautifulSoup(htmlcontent) 
        for i in range(fortimes):
            m=soup.find(id='tab2_'+str(i+1))
            print 'm is ',type(m)
            j=self.getdatatable(m.find(id='datatable'))
            print '-----------------------------'
        
    def dataanalysis(self):
        xls=openpyxl.load_workbook(u'config\\电玩捕鱼-数据分析'+self.__lastfile+'.xlsx')
        for i in self.__dataurl:
            htmlcontent=self.getcontent(self.makeurl(i.get('url')))
            if i.get('type',0)==0:
                names,data=self.beautifulsouphtml(htmlcontent)
                try:
                    sheet1=xls.get_sheet_by_name(i.get('name'))
                except:
                    sheet1=xls.create_sheet(i.get('name'))
                sheet1.append(names)
                for j in range(len(data)):
                    sheet1.append(textlistformated(data[j])) 
            elif i.get('type',0)=="mutiple":
                self.beautifulsouphtmlmultiple(htmlcontent, len(i.get('name')))
            else:
                pass
        xls.save(u'config\\电玩捕鱼-数据分析'+self.__dateend+'.xlsx')
        print 'Writing Excel Finished!!!!'
        self.__innerjson['date']['lastfile']=self.__dateend
        self.__innerjson['date']['begin']=str(date.today())
        jf=open('config\\urldata.json','w+')
        jf.write(json.dumps(self.__innerjson,ensure_ascii=False,indent=4))
        jf.close()
        print 'Writing json Finished!!!'
            
        
                