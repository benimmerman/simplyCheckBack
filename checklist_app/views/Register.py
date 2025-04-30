from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.middleware.csrf import get_token
# from rest_framework.permissions import AllowAny
# from django.urls import path


@api_view(['GET', 'POST', 'PUT'])
def register(request):
    print(request.data)
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirmPass')
        email = request.data.get('email')
        fields = [username, password, confirm_password, email]

        if not all(fields):
            return Response({'error': 'Fill all fields.'}, status=400)
        
        if password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=request.data['username'],
                                        password=request.data['password'],
                                        email=request.data['email'])
        # save to DB
        user.save()
        # sets a session id for the user, can handle safe requests such as get
        login(request, user)
        # creates csrf token that provides security for unsafe requests like post
        csrf_token = get_token(request)
        data = {'username': user.username, 'userId': user.id, 'csrfToken': csrf_token ,'message': 'login successful'}
        return Response(data , status=status.HTTP_200_OK)