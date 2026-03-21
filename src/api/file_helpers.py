import os

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def is_binary(path):
    with open(path, 'rb') as f:
        return b'\x00' in f.read(1024)

def get_extension(path):
    return os.path.splitext(path)[1]
