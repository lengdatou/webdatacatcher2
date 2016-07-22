#coding=utf-8
'''
Created on 2015年8月7日

@author: gxc
'''

import os




if __name__ == '__main__':
        os.startfile('cfg_download.bat')
        filename=raw_input('Please Enter file name:\n')
        allfiles=os.listdir('clientconfig')
        tempfiles=[]
        for i in range(len(allfiles)):
                if allfiles[i].endswith(filename+'.json')==True:
                        tempfiles.append(allfiles[i])
                        os.startfile('clientconfig\\'+allfiles[i])
        print len(tempfiles)
        print tempfiles

