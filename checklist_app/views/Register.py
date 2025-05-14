from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    confirm_pass = request.data.get("confirmPass")

    # Basic validation
    # or not email removed because it is not required
    if not username or not password or not confirm_pass:
        return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_pass:
        return Response({"message": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    # or not email removed because it is not required   
    # if User.objects.filter(email=email).exists():
    #     return Response({"message": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

    # Create user
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "User registered successfully.",
        "username": user.username,
        "userId": user.id,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }, status=status.HTTP_201_CREATED)
