from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.checklist import ListItems, Lists

@api_view(['GET'])
def dashboard(request):
  if request.method == 'GET':
    try:
      if not request.user.is_authenticated:
          return Response({'error': 'User not authenticated'}, status=401)
      
      username = request.user
      lists = Lists.objects.filter(user=username).values('listId', 'listTitle')

      return Response({'lists': list(lists)}, status=200)
    except Exception as e:

      return Response({'error': str(e)}, status=500)