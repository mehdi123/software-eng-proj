''' This module is a wrapper for Loan table in database.
 The Applicant table has these attributes:
    'loanid', 'pid', 'date', 'money', 'cheque_no', 'desc'
 In all cases, an 'info' variable means a dictionary which its keys
are these attributes.
'''

from Exceptions import *
import connection
import pub

import pythoncom
from win32com.client import constants

fields=['loanid', 'pid', 'date', 'money', 'cheque_no', 'desc']

def addLoan(info):
    ''' returns: loanid
    throws: LoanAlreadyExist '''
    
    info=info.copy()
    info['date']=pub.strToTime(info['date'])

    rs=connection.db.OpenRecordset('Loan')
    try:
        rs.AddNew()
        for key in info.keys():
            if key!='loanid':
                rs.Fields(key).Value=info[key]
        try:
            rs.Update()
        except pythoncom.com_error:
            raise LoanAlreadyExist
    finally:
        rs.Close()

    rs=connection.db.OpenRecordset('select loanid from Loan where pid=%d and date=%f'%(info['pid'], info['date']))
    try:
        rs.MoveFirst()
        return rs.Fields('loanid').Value
    finally:
        rs.Close()

def getLoanInfo(id):
    ''' returns: info
    throws: LoanNotFound '''
    
    rs=connection.db.OpenRecordset('select * from Loan where loanid='+`id`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise LoanNotFound
        info={}
        for key in fields:
            info[key]=rs.Fields(key).Value
        return info
    finally:
        rs.Close()

def getLoans():
    ' returns: a list of all \'loanid\'s in table'
    rs=connection.db.OpenRecordset('select * from Loan order by loanid')
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            return []
        loans = []
        while not rs.EOF:
            loans.append(rs.Fields('loanid').Value)
            rs.MoveNext()
        return loans
    finally:
        rs.Close()

def changeLoanInfo(info):
    ' throws: LoanNotFound'
    rs=connection.db.OpenRecordset('select * from Loan where loanid='+`info['loanid']`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise LoanNotFound
        rs.Edit()
        for key in info.keys():
            if key!='loanid' and key!='pid' and key!='date':
                rs.Fields(key).Value=info[key]
        rs.Update()
    finally:
        rs.Close()

def removeLoan(id):
    ' throws: LoanNotFound'
    rs=connection.db.OpenRecordset('select * from Loan where loanid='+`id`)
    try:
        try:
            rs.MoveFirst()
        except pythoncom.com_error:
            raise LoanNotFound
        rs.Delete()
    finally:
        rs.Close()
