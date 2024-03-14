from Blockchain.backend.core.Script import Script
from Blockchain.backend.util.util import intToLittleEndian
class CoinbaseTransaction:
    def __init__(self,BlockHeight):
        self.BlockHeightInLittleEndian = intToLittleEndian(BlockHeight)
        
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
        
        # If no script signature provided use empty one
        if scriptSignature is None:
            self.scriptSignature = Script()
        else:
            self.scriptSignature = scriptSignature

        self.sequence = sequence

class TransactionOut:
    def __init__(self,amount, scriptPublickKey):
        self.amount = amount
        self.scriptPublickKey = scriptPublickKey