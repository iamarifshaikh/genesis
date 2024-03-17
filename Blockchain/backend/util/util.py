import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log

from Blockchain.backend.core.EllepticCurve.EllepticCurve import BASE58_ALPHABET

def hash256(s):
    """Two rounds of hash25"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()

def bytesNeeded(n):
    if n == 0: 
        return 1
    return int(log(n,256)) + 1

def intToLittleEndian(n,length):
    """intToLittleEndian takes an integer and returns the little endian byte sequence of length"""
    return n.to_bytes(length, 'little')

def littleEndianToInt(b):
    """Takes a byte sequence and returns an integer"""
    return int.from_bytes(b, 'little')

def decodeBase58(s):
    num = 0

    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    
    combined = num.to_bytes(25,byteorder= 'big')
    checkSum = combined[-4:]

    if hash256(combined[:-4])[:4] != checkSum:
        raise ValueError(f"Bad Address {checkSum} {hash256(combined[:-4][:4])}")
    
    return combined[1:-4]