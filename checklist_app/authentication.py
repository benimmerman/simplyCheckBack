from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .utils.token_encryption import TokenEncryption

class EncryptedJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        try:
            # Initialize token encryption
            token_encryption = TokenEncryption()
            
            # Decrypt the token
            decrypted_token = token_encryption.decrypt_token(raw_token)
            if not decrypted_token:
                raise InvalidToken('Invalid token format')
                
            # Validate the decrypted token
            return super().get_validated_token(decrypted_token)
        except Exception as e:
            raise InvalidToken(f'Invalid token: {str(e)}') 