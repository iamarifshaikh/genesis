import hashlib

def hash256(s):

    """TWO ROUNDS OF SHA256"""
    
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()
