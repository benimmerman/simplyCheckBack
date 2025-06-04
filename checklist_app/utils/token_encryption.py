from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

class TokenEncryption:
    def __init__(self):
        # Get key from environment variable
        self.key = os.environ['ENCRYPTION_KEY'].encode()
        self.cipher_suite = Fernet(self.key)

    def encrypt_token(self, token):
        """Encrypt a token"""
        try:
            # Convert token to bytes if it's a string
            if isinstance(token, str):
                token = token.encode()
            # Encrypt the token
            encrypted_token = self.cipher_suite.encrypt(token)
            # Convert to base64 for safe transmission
            return base64.b64encode(encrypted_token).decode()
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return None

    def decrypt_token(self, encrypted_token):
        """Decrypt a token"""
        try:
            # Convert from base64
            encrypted_bytes = base64.b64decode(encrypted_token)
            # Decrypt the token
            decrypted_token = self.cipher_suite.decrypt(encrypted_bytes)
            # Convert back to string
            return decrypted_token.decode()
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            return None 