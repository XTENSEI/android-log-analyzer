import json

class JSONUtils:
    @staticmethod
    def pretty(data):
        return json.dumps(data, indent=2)
    
    @staticmethod
    def minify(data):
        return json.dumps(data, separators=(',', ':'))
    
    @staticmethod
    def merge(a, b):
        a.update(b)
        return a
