from Blockchain.Backend.core.Script import Script
from Blockchain.Backend.util.util import int_to_little_endian, bytes_needed, decode_base58, little_endian_to_int

ZERO_HASH = b'\0' * 32
REWARD = 50

PRIVATE_KEY = '30676624106278981953298788058038107283215024178469945699281606196515935662229'
MINER_KEY = '1DmhpP5jGIEjfIr9KA9fpaVcMiFWmSWfUZ'

class CoinbaseTx:
    def __init__(self, BlockHeight):
        self.BlockHeightInLittleEndian = int_to_little_endian(BlockHeight, bytes_needed(BlockHeight))

    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff

        tx_ins = []
        tx_ins.append(Tx_In(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)

        tx_outs = []
        target_amount = REWARD * 100000000
        target_h160 = decode_base58(MINER_KEY)
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(Tx_Out(amount= target_amount, script_pubkey= target_script))

        return Tx(1, tx_ins, tx_outs, 0)



class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime

    def is_coinbase(self):
        """
         # Check that there us exactly 1 input
         # Grab the first input and check if the prev_tx is b'\x00' * 32
         # Check that the first input prev_index is 0xfffffffff
        """
        if len(self.tx_ins) != 1:
            return False
        
        first_input = self.tx_ins[0]
        if first_input.prev_tx != b'\x00' * 32:
            return False
        
        if first_input.prev_index != 0xfffffffff:
            return False
        
        return True


    def to_dict(self):
        """
        CONVERT COINBASE TRANSACTION
         # Convert prev_tx Hash in hex from bytes
         # Convert Blockheight in hex which is stored in Script Signature 
        """
        
        if self.is_coinbase():
            self.tx_ins[0].prev_tx = self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0] = little_endian_to_int(self.tx_ins[0].script_sig.cmds[0])
            self.tx_ins[0].script_sig = self.tx_ins[0].script_sig.__dict__

        self.tx_ins[0] = self.tx_ins[0].__dict__

        """
        Convert transaction output into dict
         # If there are numbers we don't need to do anything
         # if values is in bytes, convert it to hex
         # loop Through all the TxOut Objects and convert them into dict
        """
        self.tx_outs[0].script_pubkey.comds[2] = self.tx_outs[0].script_pubkey.comds[2].hex()
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__

        return self.__dict__

class Tx_In:
    def __init__(self, prev_tx, prev_index, script_sig = None, sequence = 0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        
        self.sequence = sequence

class Tx_Out:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.pubkey = script_pubkey
