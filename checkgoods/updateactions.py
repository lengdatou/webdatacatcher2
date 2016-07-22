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


def updateactions():
    filename='actions'
    actionlist=json.load(file('otherjson\\16-'+filename+'.json'), 'utf-8').get('models') 
    actionarrange={'155':{'type':'all'},
                   '148':{'type':'listin',
                          'qudao':[11,13,78,79]},
                   '136':{'type':'listout',
                          'qudao':[11,13,78,79]},
                   '140':{'type':'all'},
                   '126':{'type':'all'},
                   '138':{'type':'all'}
                   }
    allfiles=os.listdir('otherjson')
    tempfiles=[]
    for i in range(len(allfiles)):
        if allfiles[i].endswith(filename+'.json')==True:
                tempfiles.append(allfiles[i])
    for j in tempfiles:
        qudao=int(j.split('-')[0])
        tempactionlist=actionlist
        for act in actionarrange.keys():
            temptype=actionarrange.get(act).get('type')
            tempqudao=actionarrange.get(act).get('qudao')
            if temptype=='all':
                continue
            elif temptype=='listin':
                if qudao in tempqudao:
                    continue
                else:
                    tempactionlist.remove
            elif temptype=='listout':
                if qudao in tempqudao:
                    tempactionlist.pop(act) 
                else:
                    continue
            else:
                print 'Error!!!!!'
        print tempactionlist            

                
updateactions()   
