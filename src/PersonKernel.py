''' This module is a wrapper for Person table in database.
 The Applicant table has these attributes:
    'pid', 'firstname', 'lastname', 'income', 'wlocation' ,'wtype', 'desc'
 In all cases, an 'info' variable means a dictionary which its keys
are these attributes.
'''

from Exceptions import *
import connection

import pythoncom
from win32com.client import constants

fields=['pid', 'firstname', 'lastname', 'income', 'wlocation' ,'wtype', 'desc']

def addPerson(info):
    ''' returns: pid
    throws: PersonAlreadyExist'''
    
    rs=connection.db.OpenRecordset('Person')
    try:
        rs.AddNew()
        for key in info.keys():
            rs.Fields(key).Value=info[key]
        try:
            rs.Update()
        except pythoncom.com_error:
            raise PersonAlreadyExist
    finally:
        rs.Close()

    rs=connection.db.OpenRecordset('select pid from Person where firstname="%s" and lastname="%s"'%(info['firstname'], info['lastname']))
    try:
        rs.MoveFirst()
        return rs.Fields('pid').Value
    finally:
        rs.Close()

def getPersonInfo(id):
    ''' returns: info
    throws: PersonNotFound. '''
    
    rs=connection.db.OpenRecordset('select * from Person where pid='+`id`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PersonNotFound
        info={}
        for key in fields:
            info[key]=rs.Fields(key).Value
        return info
    finally:
        rs.Close()

def getPersons():
    '   returns: a list of all \'pid\'s'
    rs=connection.db.OpenRecordset('select * from Person order by pid')
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            return []
        persons = []
        while not rs.EOF:
            persons.append(rs.Fields('pid').Value)
            rs.MoveNext()
        return persons
    finally:
        rs.Close()

def removePerson(id):
    '   throws: PersonNotFound'
    rs=connection.db.OpenRecordset('select * from Person where pid='+`id`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PersonNotFound
        rs.Delete()
    finally:
        rs.Close()

def changePersonInfo(info):
    '   throws: PersonNotFound'
    removePerson(info['pid'])
    addPerson(info)
