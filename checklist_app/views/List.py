from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User 
from ..models.checklist import Lists

@api_view(['POST', 'DELETE'])
def list(request):
  if request.method == 'POST':
    try:
      username = request.data['username']
      listTitle = request.data['listTitle']
      # retrieve useer from users table
      user = User.objects.get(username = username)
      # create a new row with default lilst name
      new_list = Lists(
        user_id = user.id,
        listTitle = listTitle
      )
      new_list.save()

      # data dictionary to return
      data = {'listId': new_list.listId, 'listTitle': new_list.listTitle}
      return Response(data, status=200)
    except Exception as e:
      return Response({'error': str(e)}, status=500)
    
  if request.method == 'DELETE':
    try:
        # Expecting the request to have the listId and username
        username = request.user
        list_id = request.GET.get('listId')
     
        if not username or not list_id:
            return Response({'error': 'Username and listId are required'}, status=400)

        # Retrieve the user from the users table
        user = User.objects.get(username=username)

        # Retrieve the list based on listId and check if it belongs to the user
        list_to_delete = Lists.objects.get(listId=list_id, user_id=user.id)

        # Delete the list
        list_to_delete.delete()

        return Response({'message': 'List successfully deleted'}, status=200)

    except Lists.DoesNotExist:
        return Response({'error': 'List not found'}, status=404)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=500)

