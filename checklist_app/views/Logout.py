from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from ..utils.token_encryption import TokenEncryption

@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        try:
            # Get the encrypted refresh token
            encrypted_refresh_token = request.data.get('refresh')
            
            if not encrypted_refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # First blacklist the token
            try:
                outstanding_token = OutstandingToken.objects.get(token=encrypted_refresh_token)
                BlacklistedToken.objects.get_or_create(token=outstanding_token)
            except OutstandingToken.DoesNotExist:
                pass  # Token might already be deleted
            
            # Then delete it from outstanding tokens
            OutstandingToken.objects.filter(token=encrypted_refresh_token).delete()
            
            # Clear the session
            request.session.flush()
            
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
