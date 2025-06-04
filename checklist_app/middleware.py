from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from .utils.token_encryption import TokenEncryption

class TokenRefreshMiddleware(MiddlewareMixin):
    """
    Middleware for extending JWT token expiration on successful requests.
    
    This middleware intercepts successful responses (status codes 200-299) and extends
    the expiration time of the current JWT access token. This approach is more efficient
    than generating new tokens as it:
    - Reduces database operations
    - Minimizes token blacklisting
    - Maintains session continuity
    
    Features:
        - Extends token expiration on successful requests
        - Handles both JSON and non-JSON responses
        - Gracefully handles errors without breaking the original response
        - Only processes requests with valid Bearer tokens
        - Only processes authenticated users
        - Handles encrypted tokens

    Response Format:
        For JSON responses:
            - Updates 'access' token with new expiration
        For non-JSON responses:
            - Adds 'X-New-Access-Token' header with updated token
    """
    def process_response(self, request, response):
        # Only process successful responses
        if response.status_code >= 200 and response.status_code < 300:
            # Check if the request has an Authorization header
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                try:
                    # Get the current user from the request
                    if hasattr(request, 'user') and request.user.is_authenticated:
                        # Initialize token encryption
                        token_encryption = TokenEncryption()
                        
                        # Get and decrypt the current token
                        encrypted_token = auth_header.split(' ')[1]
                        
                        token = token_encryption.decrypt_token(encrypted_token)
                        
                        if not token:
                            return response
                            
                        # Decode the token
                        access_token = AccessToken(token)
                        
                        # Print current expiration
                        current_exp = datetime.fromtimestamp(access_token['exp'])
                        
                        # Extend the token expiration by 30 minutes
                        access_token.set_exp(lifetime=timedelta(minutes=30))
                        
                        # Print new expiration
                        new_exp = datetime.fromtimestamp(access_token['exp'])
                        
                        # Encrypt the new token
                        encrypted_new_token = token_encryption.encrypt_token(str(access_token))
                        
                        # If the response is JSON, add the updated token to it
                        if isinstance(response, JsonResponse):
                            try:
                                data = json.loads(response.content)
                                data['access'] = encrypted_new_token
                                response.content = json.dumps(data)
                            except json.JSONDecodeError:
                                pass
                        else:
                            # For non-JSON responses, add token to headers
                            response['X-New-Access-Token'] = encrypted_new_token
                except Exception as e:
                    # Log the error but don't break the response
                  
                    print(f"Error type: {type(e)}")
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")
        
        return response 