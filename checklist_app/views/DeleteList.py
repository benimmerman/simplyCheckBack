from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models.checklist import Lists

@api_view(['DELETE'])
def deleteList(request):
    if request.method == 'DELETE':
        try:
            # Expecting the request to have the listId and username
            print(['request', request.GET.get('listId')])
            username = request.user
            list_id = request.GET.get('listId')
            print(username)
            print(f'list_id: {list_id}')

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

    return Response('Invalid request method', status=405)
