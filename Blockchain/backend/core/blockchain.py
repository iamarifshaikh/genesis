import sys  
sys.path.append('F:/blockchain')

from Blockchain.backend.core.block import Block
from Blockchain.backend.core.blockheader import Blockheader
from Blockchain.backend.util.util import hash256
from Blockchain.backend.core.database.database import BlockchainDB
from Blockchain.backend.core.Transaction import CoinbaseTransaction

import time

ZERO_HASH = '0' * 64
VERSION = 1

class Blockchain:
    def __init__(self):
        self.GenesisBlock()

    def writeOnDisk(self,block):
        blockchainDB = BlockchainDB()
        blockchainDB.write(block)

    def fetchLastBlock(self):
        blockchainDB = BlockchainDB()
        return blockchainDB.lastBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        prevBlockHash = ZERO_HASH
        self.addBlock(BlockHeight,prevBlockHash)

    def addBlock(self,BlockHeight,prevBlockHash):
        timestamp = int(time.time())
        coinbaseInstance = CoinbaseTransaction(BlockHeight)
        coinbaseTx = coinbaseInstance.coinBaseTransaction()
        
        # Transaction = f"Codies Alert sent {BlockHeight} Genesis To Joe"
        merkleRoot = ' '
        bits = 'ffff001f'
        blockheader = Blockheader(VERSION,prevBlockHash,merkleRoot,timestamp,bits)
        blockheader.mine()
        self.writeOnDisk([Block(BlockHeight,1,blockheader.__dict__,1,coinbaseTx.toDict()).__dict__])
        # print(json.dumps(self.chain,indent = 4))

    def main(self):
        while True:
            lastBlock = self.fetchLastBlock()
            BlockHeight = lastBlock["Height"] + 1
            prevBlockHash = lastBlock["BlockHeader"]["blockHash"]
            self.addBlock(BlockHeight,prevBlockHash)

if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()