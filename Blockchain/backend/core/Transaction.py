import sys  
sys.path.append('F:/blockchain')
from Blockchain.backend.core.Script import Script
from Blockchain.backend.util.util import intToLittleEndian, bytesNeeded,decodeBase58, littleEndianToInt

ZERO_HASH = b'\0' * 32
REWARD = 50

PRIVATE_KEY = '4379043949018181181415408087195683991292678849717025934098747731947970339496'
MINERS_ADDRESS = '1LYgXwYXw16GJXgDwHV7aCNijnQWYEdc1C'
class CoinbaseTransaction:
    def __init__(self,BlockHeight):
        self.BlockHeightInLittleEndian = intToLittleEndian(BlockHeight,bytesNeeded(BlockHeight))

    def coinBaseTransaction(self):
        previousTransaction = ZERO_HASH
        previousIndex = 0xffffffff

        transactionIns = []
        transactionIns.append(TransactionIn(previousTransaction,previousIndex))
        transactionIns[0].scriptSignature.cmds.append(self.BlockHeightInLittleEndian)

        transactionOuts = []
        targetAmount = REWARD * 100000000
        targetH160 = decodeBase58(MINERS_ADDRESS)
        targetScript = Script.p2pkhScript(targetH160)
        transactionOuts.append(TransactionOut(amount=targetAmount,scriptPublicKey=targetScript))

        return Transaction(1,transactionIns,transactionOuts, 0)

class Transaction:
    def __init__(self,version,transactionIns,transactionOuts,locktime):
        self.version = version
        self.transactionIns = transactionIns
        self.transactionOuts = transactionOuts
        self.locktime = locktime

    def isCoinbase(self):
        """
        # Check that there is exactly 1 input
        # Grab the first input and check if the previousTransaction is b'\x00' * 32
        # Check that the first input previousIndex is 0xffffffff
        """

        if len(self.transactionIns)!= 1:
            return False
        
        firstInput = self.transactionIns[0]

        if firstInput.prevTransaction!= ZERO_HASH:
            return False
        
        if firstInput.prevIndex!= 0xffffffff:
            return False
        
        return True

    def toDict(self):
        """
        Convert Coinbase Transaction
            # Convert previous transaction Hash in hex from bytes
            # Convert Blockheight in hex which is stored in Script Signature
        """

        if self.isCoinbase():
            self.transactionIns[0].prevTransaction = self.transactionIns[0].prevTransaction.hex()
            self.transactionIns[0].scriptSignature.cmds = littleEndianToInt(self.transactionIns[0].scriptSignature.cmds[0])
            self.transactionIns[0].scriptSignature = self.transactionIns[0].scriptSignature.__dict__
        
        self.transactionIns[0] = self.transactionIns[0].__dict__

        """
        Convert Transaction Output to dict
        # If there are Numbers we don't need to do anything
        # If values is in bytes, convert it to hex
        # Loop Through all the TxOut Objects and convert them into dict
        """
        self.transactionOuts[0].scriptPublicKey.cmds[2] = self.transactionOuts[0].scriptPublicKey.cmds[2].hex()
        self.transactionOuts[0].scriptPublicKey = self.transactionOuts[0].scriptPublicKey.__dict__
        self.transactionOuts[0] = self.transactionOuts[0].__dict__

        return self.__dict__

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
    def __init__(self,amount, scriptPublicKey):
        self.amount = amount
        self.scriptPublicKey = scriptPublicKey