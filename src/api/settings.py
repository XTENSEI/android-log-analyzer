import json
import os

class Settings:
    def __init__(self, path='settings.json'):
        self.path = path
        self.data = self.load()
    
    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                return json.load(f)
        return self.defaults()
    
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def defaults(self):
        return {
            'theme': 'dark',
            'language': 'en',
            'autoAnalyze': True,
            'maxFileSize': 500
        }
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
        self.save()
