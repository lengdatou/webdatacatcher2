# -*- coding:utf-8 -*- 
'''
Created on 2016��7��21��

@author: legnwei
'''

def textlistformated(textlist):
    outlist=list()
    for i in textlist:
        if i.isdigit()==True:
            i=float(i)
        elif i.endswith('%'):
            i=float(i.split('%')[0])/100
        elif i.find('.')>0:
            i=float(i)
        elif i.find('-')>0 and len(i)<=10:
            i=i.split('-')
            i=i[0]+'/'+str(int(i[1]))+'/'+str(int(i[2]))
        else:
            pass
        outlist.append(i)
    return outlist