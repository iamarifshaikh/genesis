import hashlib

def hash256(s):
    """Two rounds of hash25"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()