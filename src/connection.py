' This module handles connection to the database.'

import win32com.client

class AlreadyOpen(Exception):
    pass
class AlreadyClosed(Exception):
    pass

engine=win32com.client.Dispatch('DAO.DBEngine.36')
db=engine.OpenDatabase('Bank.mdb')
_closed=0

def close():
    'Closes connection to the database.'
    
    global _closed
    if _closed:
        raise AlreadyClosed
    db.Close()
    _closed=1

def open():
    'Opens connection to the database.'
    
    global db, _closed
    if not _closed:
        raise AlreadyOpen
    db=engine.OpenDatabase('Bank.mdb')
    _closed=0
