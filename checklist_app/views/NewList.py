from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User 
from ..models.checklist import Lists

@api_view(['POST'])
def createNewList(request):
  if request.method == 'POST':
    print(request.data)
    try:
      username = request.data['username']
      # retrieve useer from users table
      user = User.objects.get(username = username)
      # create a new row with default lilst name
      new_list = Lists(
        user_id = user.id,
      )
      new_list.save()

      # data dictionary to return
      data = {'listID': new_list.listId, 'listTitle': new_list.listTitle}

      return Response(data, status=200)
    except Exception as e:
      print(e)
      return Response({'error': str(e)}, status=500)
  return Response('did not execute')