from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def credentials(request):
  if request.method == 'POST':

    username = request.data['username']
    password = request.data['password']
    # creates a new user in the auth_user table from restframework. gives each user unique user id in field "id"
    user = authenticate(request, 
                        username = username, 
                        password = password)
      
    if user is not None:
      # sets a session id for the user, can handle safe requests such as get
      login(request, user)
      token = Token.objects.create(user=user)
      print(token.key)
      data = {'username': user.username, 'userId': user.id, 'message': 'login successful'}
      print(data)
      return Response(data, status=status.HTTP_200_OK)
    else:
      # return invalid so frontend knows credentials did not match
      return Response({'message': 'Login failed. Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)