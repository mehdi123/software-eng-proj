' This module contains common exceptions used in other modules.'

class PersonAlreadyExist(Exception):
    pass

class PersonNotFound(Exception):
    pass

class LoanAlreadyExist(Exception):
    pass

class LoanNotFound(Exception):
    pass

class GenerousAlreadyExist(Exception):
    pass

class GenerousNotFound(Exception):
    pass

class PaymentAlreadyExist(Exception):
    pass

class PaymentNotFound(Exception):
    pass
