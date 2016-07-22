#coding=utf-8
'''
Created on 2015年10月29日

@author: lengwei
'''

import os
import xlrd
import codecs
import json

configfile=xlrd.open_workbook(u"金蟾捕鱼2_三期版本_数值_release.xlsx").sheet_by_name("export")
filecount=int(configfile.cell_value(0,3))
print ("Total json files is %d"%filecount)
#最后一行文件对应的excel行号

configfile_folder = configfile.col_values(0,1,filecount)
configfile_name   = configfile.col_values(1,1,filecount)
configfile_values = configfile.col_values(2,1,filecount)

for j in configfile_name:
	print j

for i in range(filecount-1):
	filepath=configfile_folder[i]+'\\'+configfile_name[i]+'.json'
	filejson=codecs.open(filepath,"w+","utf-8")
	filejson.writelines(configfile_values[i])
	filejson.close()
	obj = json.load(file(filepath),"utf-8")
	filejson=codecs.open(filepath,"w+","utf-8")
	obj_formated = json.dumps(obj,ensure_ascii=False,indent=4)
	filejson.writelines(obj_formated)
	filejson.close()

os.system("validjson.py")

raw_input()

#obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]
#encodedjson = json.dumps(obj)
#print repr(obj)
#print encodedjson
