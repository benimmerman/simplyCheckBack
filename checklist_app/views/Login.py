from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    summary="User Login",
    description=""" 
    Handle user authentication and login.

    This endpoint authenticates users and returns their session information.
    It uses Django's authentication system to verify credentials and creates
    a session for the authenticated user. """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'},
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'access': {'type': 'string'},
                'refresh': {'type': 'string'},
                'username': {'type': 'string'},
                'userId': {'type': 'integer'},
                'message': {'type': 'string'}
            }
        },
     
        401: {
            'type': 'object',
            'properties': {
                'detail': {'type': 'string'},
            }
        }
    },
    examples=[
        OpenApiExample(
            'Success Response',
            value={
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'username': 'user123',
                'userId': 1,
                'message': 'login successful'
            },
            status_codes=['200']
        ),
        OpenApiExample(
            'Error Response',
            value={'message': 'Login failed. Invalid username or password.'},
            status_codes=['401']
        ),
    ]
)
@api_view(['POST'])

def credentials(request):
    """
    Handle user authentication and login.

    This endpoint authenticates users and returns their session information.
    It uses Django's authentication system to verify credentials and creates
    a session for the authenticated user.

   
    """
    if request.method == 'POST':
      # retrieve username and password from request
      username = request.data.get('username')
      password = request.data.get('password')

      # authenticate user
      user = authenticate(request, username=username, password=password)
      
      if user is not None:
          # login user
          login(request, user)
          # create refresh token
          refresh = RefreshToken.for_user(user)
          # return response
          return Response({
              'access': str(refresh.access_token),
              'refresh': str(refresh),
              'username': user.username,
              'userId': user.id,
              'message': 'login successful'
          }, status=status.HTTP_200_OK)
      else:
          # return error response
          return Response(
              {'message': 'Login failed. Invalid username or password.'},
              status=status.HTTP_401_UNAUTHORIZED
          )