from abc import ABCMeta, abstractmethod, abstractproperty

class Transaction(object):
    """docstring for Transaction"""
    def __init(self):
        self.child_transaction = None

    def is_success(self):
        pass

    def is_faile(self):
        pass

    def start(self):
        pass

    def has_child_transaction(self):
        return self.child_transaction is not None

    def get_child_transaction(self):
        return self.child_transaction

    def set_child_transaction(self, transaction):
        if not isinstance(transaction, Transaction) : return False
        if not self.has_child_transaction():
            self.child_transaction = transaction
        else:
            self.child_transaction.set_child_transaction(transaction)

class TransactionExecutor(object):
    """docstring for TransactionExecutor"""
    def __init__(self):
        super(TransactionExecutor, self).__init__()



class Test(Transaction):
    """docstring for Test"""
    def __init__(self):
        super(Test, self).__init__()


t = Test()
print isinstance(t, Transaction)
print hasattr(t, 'is_success')
