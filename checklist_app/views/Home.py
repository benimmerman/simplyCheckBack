from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.checklist import ListItems, Lists
# from django.views.decorators.csrf import csrf_exempt


# @api_view(['GET'])
# def dashboard(request):
#   if request.method == 'GET':
#     lists = Lists.objects.all()
#     print(request)
#     print('home')
#     return Response({'message': 'django home'})

@api_view(['GET'])
def dashboard(request):
  print(request.user)
  print(request.headers)
  print(request.auth)
  if not request.user.is_authenticated:
      return Response({'error': 'User not authenticated'}, status=401)
  
  user = request.user
  lists = Lists.objects.filter(user=user).values('listId', 'listTitle')
  print('lists:', lists)

  return Response({'lists': list(lists)}, status=200)