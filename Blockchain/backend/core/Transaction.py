class Transaction:
    def __init__(self,version,transactionIns,transactionOuts,locktime):
        self.version = version
        self.transactionIns = transactionIns
        self.transactionOuts = transactionOuts
        self.locktime = locktime

class TransactionIn:
    def __init__(self,prevTransaction,prevIndex,scriptSignature = None,sequence = 0xffffffff):
        self.prevTransaction = prevTransaction
        self.prevIndex = prevIndex
        
        self.scriptSignature = scriptSignature
        self.sequence = sequence