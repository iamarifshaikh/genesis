import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256

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
