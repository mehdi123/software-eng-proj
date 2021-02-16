''' This module is a wrapper for Applicant table in database.
 The Applicant table has these attributes:
    'pid', 'money', 'numofpays', 'date', 'univ_debt' ,'desc'
 In all cases, an 'info' variable means a dictionary which its keys
are these attributes.
'''

from Exceptions import *
import connection

import pythoncom
from win32com.client import constants

fields=['pid', 'money', 'numofpays', 'date', 'univ_debt' ,'desc']

def addApplicant(info):
    ''' returns: pid
    throws: PersonAlreadyExist '''
    find=connection.db.OpenRecordset('select * from Applicant where pid='+`info['pid']`)
    rs=None
    try:
        found=1
        try:
            find.MoveFirst()
        except pythoncom.com_error:
            found=0
        if found:
            raise PersonAlreadyExist

        rs=connection.db.OpenRecordset('Applicant')
        rs.AddNew()
        for key in info.keys():
            rs.Fields(key).Value=info[key]
        rs.Update()
    finally:
        find.Close()
        try:
            rs.Close()
        except AttributeError:
            pass

def getApplicantInfo(id):
    ''' returns: info
    throws: PersonNotFound '''
    rs=connection.db.OpenRecordset('select * from Applicant where pid='+`id`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PersonNotFound
        info={}
        for key in fields:
            info[key] = rs.Fields(key).Value
        return info
    finally:
        rs.Close()

def getApplicants():
    ''' returns: a list of all 'pid's '''
    rs=connection.db.OpenRecordset('select * from Applicant order by pid')
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            return []
        apps=[]
        while not rs.EOF:
            apps.append(rs.Fields('pid').Value)
            rs.MoveNext()
        return apps
    finally:
        rs.Close()

def changeApplicantInfo(info):
    '   throws: PersonNotFound '
    rs=connection.db.OpenRecordset('select * from Applicant where pid='+`info['pid']`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PersonNotFound
        rs.Edit()
        for key in info.keys():
            if key!='pid':
                rs.Fields(key).Value=info[key]
        rs.Update()
    finally:
        rs.Close()

def removeApplicant(id):
    '   throws: PersonNotFound '
    rs=connection.db.OpenRecordset('select * from Applicant where pid='+`id`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PersonNotFound
        rs.Delete()
    finally:
        rs.Close()
