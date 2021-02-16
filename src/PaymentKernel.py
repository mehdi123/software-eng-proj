''' This module is a wrapper for Payment table in database.
 The Applicant table has these attributes:
    'loanid', 'money', 'date', 'cheque_no', 'desc'
 In all cases, an 'info' variable means a dictionary which its keys
are these attributes.
'''

from Exceptions import *
import connection
import pub

import pythoncom
from win32com.client import constants

fields=['loanid', 'money', 'date', 'cheque_no', 'desc']

def addPayment(info):
    '   throws: PaymentAlreadyExist'
    info=info.copy()
    info['date']=pub.strToTime(info['date'])

    rs=connection.db.OpenRecordset('Payment')
    try:
        rs.AddNew()
        for key in info.keys():
            rs.Fields(key).Value=info[key]
        try:
            rs.Update()
        except pythoncom.com_error:
            raise PaymentAlreadyExist
    finally:
        rs.Close()

def getPaymentInfo(loanid, date):
    ''' returns: info
    throws: PaymentNotFound '''
    
    date=pub.strToTime(date)
    rs=connection.db.OpenRecordset('select * from Payment where loanid=%d and date=%f'%(loanid, date))
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PaymentNotFound
        info={}
        for key in fields:
            info[key] = rs.Fields(key).Value
        return info
    finally:
        rs.Close()

def getPayments():
    '   returns: a list of dictionaries with [\'loanid\', \'date\'] keys'
    rs=connection.db.OpenRecordset('select * from Payment order by loanid')
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            return []
        pays = []
        while not rs.EOF:
            pays.append({'loanid':rs.Fields('loanid').Value,
                         'date':rs.Fields('date').Value})
            rs.MoveNext()
        return pays
    finally:
        rs.Close()

def changePaymentInfo(info):
    ' throws: PaymentNotFound'
    info=info.copy()
    info['date']=pub.strToTime(info['date'])
    rs=connection.db.OpenRecordset('select * from Payment where loanid=%d and date=%f'%(info['loanid'], info['date']))
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PaymentNotFound
        rs.Edit()
        for key in info.keys():
            if key!='loanid' and key!='date':
                rs.Fields(key).Value=info[key]
        rs.Update()
    finally:
        rs.Close()

def removePayment(loanid, date):
    '   throws: PaymentNotFound'
    date=pub.strToTime(date)
    rs=connection.db.OpenRecordset('select * from Payment where loanid=%d and date=%f'%(loanid, date))
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise PaymentNotFound
        rs.Delete()
    finally:
        rs.Close()
