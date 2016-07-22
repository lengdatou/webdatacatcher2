#coding:utf-8
'''
Created on 2016/05/06

@author: lengwei
'''

import Tkinter as tk
from propmodify import PropHandler,Return_keyvaluelist
import ttk
import tkMessageBox as tkmbox
import string
from ScrolledText import ScrolledText
import json
from Tkinter import IntVar


tk_title='数据查询'

databsejson=json.load(file("config\\database.json"), "utf-8")
defaultdbname=databsejson['defaultdbname']
tk_dbnamelist=databsejson['dbnamelist']
PADY=5



def MessageBox_type(title='你没给标题呀！！', message='你没给文本啊！！！！', showtype='info',**options):
    if showtype=='info':
        tkmbox.showinfo(title, message,**options)
    elif showtype=='waring':
        tkmbox.showwarning(title, message,**options)
    elif showtype=='error':
        tkmbox.showerror(title, message,**options)
    elif showtype=='question':
        tkmbox.askquestion(title, message,**options)
    elif showtype=='okcancel':
        tkmbox.askokcancel(title, message,**options)
    elif showtype=='yesno':
        tkmbox.askyesno(title, message,**options)
    elif showtype=='yesnocancel':
        tkmbox.askyesnocancel(title, message,**options) 
    elif showtype=='retrycancel':
        tkmbox.askretrycancel(title, message,**options)        
                 

class Label_Combobox(ttk.Frame):
    def __init__(self, master=None,labelshow='', textshow='readonly',valueshow='',**kw):
        ttk.Frame.__init__(self, master=None, **kw)
        ttk.Label(self,text=labelshow).pack(anchor = 'nw',side = 'left',padx=5,pady=7)
        self.__ComboText = ttk.Combobox(self,values= valueshow,state=textshow,width=15)
        self.__ComboText.set(valueshow[0])
        self.__ComboText.pack(anchor = 'nw',side = 'left',padx=5,pady=5)
        
    def getvalue(self):
        return string.strip(self.__ComboText.get())
    
    def setvalue(self,newvalue):
        self.__ComboText.set(newvalue)
    
class Label_Entry(ttk.Frame):
    def __init__(self, master=None,labelshow='',**kw):
        ttk.Frame.__init__(self, master=None, **kw)
        ttk.Label(self,text=labelshow).pack(anchor = 'nw',side = 'left',padx=5,pady=7)
        self.__EntryText = ttk.Entry(self,width=10)#,validate='all',validatecommand=self.checkvalidate,invalidcommand=self.invalidatehandle)
        self.__EntryText.pack(anchor = 'nw',side = 'left',padx=5,pady=5)
        
    def getvalue(self):
        return string.strip(self.__EntryText.get())
    
    def checkvalidate(self):
        checkstr=self.__EntryText.get()
        print checkstr
        if checkstr.isdigit()==True:
            return True
        else:
            return False
        
    def invalidatehandle(self):
        MessageBox_type('Warning!!!', 'numbers only!!!', 'warning')    


class Toplevel_ScolledText(tk.Toplevel):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Toplevel.__init__(self, master=None, cnf={}, **kw)
        self.__ShowText = ScrolledText(self,height = 20,width=40)
        self.__ShowText.pack(expand=1,fill='both')
        
    def addtext(self,Text_output=''):
        self.__ShowText.insert('end',Text_output)
        print(Text_output)
        
class RadioButtonlist(ttk.Frame):
    def __init__(self,master=None,buttonnamelist=[],**kw):
        ttk.Frame.__init__(self, master=None, **kw)
        self.__buttonlist=[]
        self.__vat= IntVar()
        self.__vat.set(0)
        for i in range(len(buttonnamelist)):
            self.__buttonlist.append(ttk.Radiobutton(self,text=buttonnamelist[i],variable=self.__vat,value=i))
            self.__buttonlist[i].pack(anchor = 'nw',side = 'left',padx=5,pady=5)
    
    def getvalue(self):
        return self.__vat.get()

               
class MyTk():
    def __init__(self):
        self.__mytk=tk.Tk()
        self.__makewindow(tk_title)
        self.__listbox_selectdb=Label_Combobox(self.__mytk,labelshow='数据库',valueshow=tk_dbnamelist)
        self.__listbox_selectdb.setvalue(defaultdbname)
        self.__prophandler=PropHandler(self.__listbox_selectdb.getvalue())
        self.__button_addprops=ttk.Button(self.__mytk,text='添加全部道具',command=self.__callback_addprops)
        self.__entry_uid=Label_Entry(self.__mytk,labelshow='UID')
        self.__listbox_propid=Label_Combobox(self.__mytk,labelshow='道具名称',valueshow=Return_keyvaluelist(self.__prophandler.getproplist()))
        self.__listbox_propnum=Label_Combobox(self.__mytk,labelshow='道具数量',valueshow=[1,10,50,100,1000,5000,0])                   
        self.__button_updateproplist=ttk.Button(self.__mytk,text='更新道具列表',command=self.createproplist)
        self.__button_addcertainprop=ttk.Button(self.__mytk,text='添加指定道具',command=self.__callback_addcertainprop)
        self.__entry_moneyordiamond=Label_Entry(self.__mytk,labelshow='金币/钻石/奖券数量')
        self.__button_addmoneyanddiamond=ttk.Button(self.__mytk,text='添加金币钻石奖券',command=self.__callback_addmoneyanddiamond)
        self.__ratiobutton_money=RadioButtonlist(self.__mytk,buttonnamelist=['金币','钻石','奖券'])        
        self.__allpack()
        self.__prophandler.getdb().mycloseconnection()
        self.__mytk.mainloop()
    
    def __allpack(self):
        self.__listbox_selectdb.pack(pady=PADY)
        self.__entry_uid.pack(pady=PADY)
        self.__entry_moneyordiamond.pack(pady=PADY)
        self.__ratiobutton_money.pack(pady=PADY)
        self.__button_addmoneyanddiamond.pack(pady=PADY)
        self.__button_addprops.pack(pady=PADY)
        self.__button_addcertainprop.pack(pady=PADY)
        self.__listbox_propnum.pack(pady=PADY)        
        self.__button_updateproplist.pack(pady=PADY)        
        self.__listbox_propid.pack(pady=PADY)
    
    def __makewindow(self,title='你没给标题呀！！！',resizeablearg=[False,False]):
        self.__mytk.title(title)
        w=self.__mytk.winfo_screenwidth()
        h=self.__mytk.winfo_screenheight()
        geom='500x500+%d+%d'%(w/2-250,h/2-250)
        self.__mytk.geometry(geom)
        self.__mytk.resizable(width=resizeablearg[0], height=resizeablearg[1])
    
    def createproplist(self):
        getdbname=self.__listbox_selectdb.getvalue()
        if getdbname in ['fish3','fish3-dev']:
            self.__prophandler.changeproplist("config\\prop_FISH.json")
        else:
            self.__prophandler.changeproplist("config\\prop_DWC.json")
        if self.__listbox_propid!=None:
            self.__listbox_propid.destroy()
        self.__listbox_propid=Label_Combobox(self.__mytk,labelshow='道具名称',valueshow=Return_keyvaluelist(self.__prophandler.getproplist()))
        self.__listbox_propid.pack(pady=10)       
    
    def dbcompare(self):
        getdbname=self.__listbox_selectdb.getvalue()
        compdbname=self.__prophandler.getdb().defaultdbname
        if compdbname!=getdbname:
            self.__prophandler.getdb().mychangedb(getdbname)
            if self.__listbox_selectdb.getvalue() in ['fish3','fish3-dev']:
                self.__prophandler.changeproplist("config\\prop_FISH.json")
            else:
                self.__prophandler.changeproplist("config\\prop_DWC.json")
        
    def __callback_addprops(self):
        self.dbcompare()
        getuid=self.__entry_uid.getvalue()
        getpropnum=self.__listbox_propnum.getvalue()
        addresult=self.__prophandler.addallprops(getuid,getpropnum)
        if addresult==True:
            MessageBox_type('操作结果', '成功！！！')
        else:
            MessageBox_type('操作结果', '失败！！！UID为空或者不存在')
            
    def __callback_addcertainprop(self):
        self.dbcompare()
        getpropid=self.__prophandler.returnnametopropid(self.__listbox_propid.getvalue())
        getuid=self.__entry_uid.getvalue()
        getpropnum=self.__listbox_propnum.getvalue()
        addresult=self.__prophandler.updateprops(getuid, getpropid, getpropnum)
        if addresult==True:
            MessageBox_type('操作结果', '成功！！！')
        else:
            MessageBox_type('操作结果', '失败！！！')

    def __callback_addmoneyanddiamond(self):
        self.dbcompare()
        getuid=self.__entry_uid.getvalue()
        getnum=self.__entry_moneyordiamond.getvalue()
        gettype=self.__ratiobutton_money.getvalue()
        addresult=self.__prophandler.addmoneyanddiamond(getuid, getnum,gettype)
        if addresult==True:
            MessageBox_type('操作结果', '成功！！！')
        else:
            MessageBox_type('操作结果', '失败！！！')
        
    