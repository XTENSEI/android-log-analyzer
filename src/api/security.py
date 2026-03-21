import hashlib
import hmac
import secrets

class Security:
    @staticmethod
    def generate_token(length=32):
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_password(password):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()
    
    @staticmethod
    def verify_password(password, hashed):
        return hmac.compare_digest(
            hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex(),
            hashed
        )
    
    @staticmethod
    def generate_api_key():
        return f"la_{secrets.token_urlsafe(32)}"
