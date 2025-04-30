from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import get_token

@api_view(['GET'])
def get_csrf_token(request):
    token = get_token(request)
    print(token)
    return Response({'csrfToken': token})