import hashlib
import time

class Hasher:
    @staticmethod
    def md5(data):
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def sha256(data):
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def timestamp():
        return str(int(time.time()))
