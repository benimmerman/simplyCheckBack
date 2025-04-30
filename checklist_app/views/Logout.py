from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
# from django.views.decorators.csrf import csrf_protect

# @csrf_protect
@api_view(['POST'])
def logout_view(request):
    logout(request)  # Clears the session
    return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
