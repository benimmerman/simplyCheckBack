from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import datetime, timedelta
from ..utils.token_encryption import TokenEncryption

class EncryptedTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Get the original response from the parent class
        response = super().post(request, *args, **kwargs)
        
        # Initialize token encryption
        token_encryption = TokenEncryption()
        
        # Get the tokens from the response
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        
        if access_token and refresh_token:
            # Encrypt both tokens
            encrypted_access = token_encryption.encrypt_token(access_token)
            encrypted_refresh = token_encryption.encrypt_token(refresh_token)
            
            # Update the response with encrypted tokens
            response.data['access'] = encrypted_access
            response.data['refresh'] = encrypted_refresh
            
        return response

class EncryptedTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Initialize token encryption
        token_encryption = TokenEncryption()
        
        # Get and decrypt the refresh token
        encrypted_refresh = request.data.get('refresh')
        if not encrypted_refresh:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        refresh_token = token_encryption.decrypt_token(encrypted_refresh)
        if not refresh_token:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Update request data with decrypted token
        request.data['refresh'] = refresh_token
        
        # Get the original response
        response = super().post(request, *args, **kwargs)
        
        # Encrypt the new access token
        if 'access' in response.data:
            response.data['access'] = token_encryption.encrypt_token(response.data['access'])
            
        return response
