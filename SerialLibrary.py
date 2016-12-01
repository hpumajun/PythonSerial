#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Purpose:     Economic Indoor Autotest Python Script
#
# Author:      ronghuihui
# Created:     2016-07-01
# Version:     0.1
# Copyright:   (c) Hikvision.com 2013
#---------------------------------------------------------
import os
import sys
import serial
from time import *
import logging
import traceback
from serial.serialwin32 import Serial

from serial.serialutil import *
from robot.api import logger

import thread


class IndoorException(Exception):
    
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
        
 
class serialinfo(object):
    def __init__(self):
        self.port = None
        self.baudrate = None
        self.timeout = 0.01
    def setvalue(self,port,baudrate):
        self.port = port
        self.baudrate = baudrate


class SerialOperate(Serial):
    
    def __init__(self, developer_email="majun11@hikvision.com.cn"):        
        self.developer_email=developer_email
        self.console = None
        self.outputinfo = ''
        self.cmd = ''

    def open_serial(self,*args, **kwargs):
        try:
            self.console = Serial(*args, **kwargs)
        except Exception as e: 
            raise IndoorException("open serial failed")
        if self.console.isOpen():
            logging.info(u'[ open serial successfully\n')
        else:
            logging.info(u'[open serial failed\n')
        return self.console
    
    def exec_cmd(self,cmd):
        cmd = str(cmd)
        cmd += "\n"
        self.console.flushInput() 
        try:
            self.console.write(cmd) 
            traceback.print_exc()
        except Exception, e:
            logging.error(u"Write error")
        self.console.flushOutput()
        sleep(0.4)
#         return self.console.read(200)

    def close_serial(self):
        self.console.close()
        
    def output_read(self):
        info = ''
        x = self.console.read(1024)   # x is str type
        info = info + x
        return info
    
    def readoutputforever(self):
        while(1):
            info = self.output_read()
            if (info != ''):
                self.outputinfo += info
                
    def ReadOutTask(self):
        thread.start_new_thread(self.readoutputforever,())
    
    def sendcmdtask(self):
        while(1):
            if(self.cmd == None):
                self.exec_cmd(self.cmd)
                self.cmd = None                
    
    def sendcmd(self,string):
        self.cmd = string
              
    def readcmdoutput(self):
        output = self.outputinfo
        self.outputinfo = ''
        return output
            
if __name__ == '__main__':

#     print os.name
#     print sys.platform
#     
    t = SerialOperate()
    # we must set timeout, or it will block to read untill reach the bytes your required
    
    t.open_serial('com1',115200,timeout = 0.2)
    t.ReadOutTask()
#     t.readoutputforever()
    for i in range (1,10):
        t.exec_cmd("openvpn")
        print "**%s**" % t.readcmdoutput()
        sleep(1)
    thread.exit()
    t.close_serial()
