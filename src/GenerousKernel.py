''' This module is a wrapper for Generous table in database.
 The Applicant table has these attributes:
    'pid', 'money', 'date', 'cheque_no', 'desc'
 In all cases, an 'info' variable means a dictionary which its keys
are these attributes.
'''

from Exceptions import *
import connection
import pub

import pythoncom
from win32com.client import constants

fields=['pid', 'money', 'date', 'cheque_no', 'desc']

def addGener(info):
    '   throws: GenerousNotFound'
    info=info.copy()
    info['date']=pub.strToTime(info['date'])
    rs=connection.db.OpenRecordset('Generous')
    try:
        rs.AddNew()
        for key in info.keys():
            rs.Fields(key).Value=info[key]
        try:
            rs.Update()
        except pythoncom.com_error:
            raise GenerousAlreadyExist
    finally:
        rs.Close()

def getGenerInfo(pid, date):
    ''' returns: info
    throws: GenerousNotFound '''

    date=pub.strToTime(date)
    rs=connection.db.OpenRecordset('select * from Generous where pid=%d and date=%f'%(pid, date))
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise GenerousNotFound
        info={}
        for key in fields:
            info[key]=rs.Fields(key).Value
        return info
    finally:
        rs.Close()

def getGeners():
    '   returns: a list of dictionaries with [\'pid\', \'date\'] keys'
    
    rs=connection.db.OpenRecordset('select * from Generous order by pid')
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            return []
        geners = []
        while not rs.EOF:
            geners.append({'pid':rs.Fields('pid').Value,
                           'date':rs.Fields('date').Value})
            rs.MoveNext()
        return geners
    finally:
        rs.Close()

def removeGener(pid, date):
    '   throws: GenerousNotFound'
    date=pub.strToTime(date)
    rs=connection.db.OpenRecordset('select * from Generous where pid=%d and date=%f'%(pid, date))
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise GenerousNotFound
        rs.Delete()
    finally:
        rs.Close()

def changeGenerInfo(info):
    removeGener(info['pid'], info['date'])
    addGener(info)