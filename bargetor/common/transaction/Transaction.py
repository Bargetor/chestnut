from abc import ABCMeta, abstractmethod, abstractproperty

class Transaction(object):
    """docstring for Transaction"""

    def is_success():
        pass

    def is_faile():
        pass

    def start():
        pass

    def has_child_transaction():
        pass

    def get_child_transaction():
        pass



class Test(Transaction):
    """docstring for Test"""
    def __init__(self):
        super(Test, self).__init__()


t = Test()
print isinstance(t, Transaction)
print hasattr(t, 'is_success')
