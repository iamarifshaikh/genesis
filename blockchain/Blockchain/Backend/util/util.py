import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log

from Blockchain.Backend.core.EllepticCurve.EllepticCurve import BASE58_ALPHABET

def hash256(s):

    """TWO ROUNDS OF SHA256"""
    
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def hash160(s):
    
    return RIPEMD160.new(sha256(s).digest()).digest()

def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1

def int_to_little_endian(n, length):
    """Int_to_LITTLE_ENDIAN TAKES INTEGER AND RETURNS THE LITTLE_ENDIAN BYTE SEQUENCE OF LENGTH"""
    return n.to_bytes(length, 'little')

def little_endian_to_int(b):
    """Takes a bytes sequence and returns an integer"""
    return int.from_bytes(b, 'little')

def decode_base58(s):
    num = 0
    
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder= 'big')
    checksum = combined[-4:]

    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f'Bad address {checksum} {hash256(combined[:-4][:4])}')
    
    return combined[1:-4]

    
