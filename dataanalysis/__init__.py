#coding:utf-8
'''
Created on 2016/07/09

@author: lengwei
'''

from analysis import *



if __name__=='__main__':
    for i in datelist:
        treasure_log(i,"G")
        treasure_log(i,"D")
    #aaa=json.JSONEncoder().encode(itemdate)
    filejson=codecs.open('treasure_log.json',"w+","utf-8")
    obj_formated = json.dumps(itemdate,ensure_ascii=False,indent=4)
    filejson.writelines(obj_formated)    
    filejson.close()    
    print obj_formated