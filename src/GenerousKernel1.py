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

def getGenerInfo(generact):
    ''' returns: info
    throws: GenerousNotFound '''

    rs=connection.db.OpenRecordset('select * from Generous where generact=%d'%(generact))
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
    '   returns: a list of generact'
    
    rs=connection.db.OpenRecordset('select generact from Generous order by generact')
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            return []
        geners = []
        while not rs.EOF:
            geners.append(rs.Fields('generact').Value)
            rs.MoveNext()
        return geners
    finally:
        rs.Close()

def removeGener(generact):
    '   throws: GenerousNotFound'
    rs=connection.db.OpenRecordset('select * from Generous where generact=%d'%(generact))
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise GenerousNotFound
        rs.Delete()
    finally:
        rs.Close()

def changeGenerInfo(info):
    '   throws: GenerousNotFound'
    
    removeGener(info['generact'])
    addGener(info)
