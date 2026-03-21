import os

def get_system_info():
    return {
        'platform': os.name,
        'cwd': os.getcwd(),
        'user': os.getenv('USER', 'unknown'),
        'home': os.path.expanduser('~')
    }

def get_env(key, default=None):
    return os.getenv(key, default)
