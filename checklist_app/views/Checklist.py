from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User 
from ..models.checklist import ListItems, Lists 
from django.utils import timezone

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def checklist(request, username=None, list_id=None):
    
    if request.method == 'GET':
        
        if not username or not list_id:
            return Response({'error': 'Username and list ID are required'}, status=400)
        try:
            # Retrieve the user from the users table
            user = User.objects.get(username=username)
            print('userid', user.id)
            # Retrieve the list based on listId and check if it belongs to the user
            list_obj = Lists.objects.get(listId=list_id, user_id=user.id)
            items = ListItems.objects.filter(listId=list_obj.listId)
            item_data = list(items.values('id', 'itemName', 'isDone', 'notes', 'createdWhen'))
            print(item_data)
            return Response({'listItems': item_data, 'listTitle': list_obj.listTitle},status=200)
        except Exception as e:
            print(e)
            return Response(e)
        
    if request.method == 'POST':
        print('request.data:',request.data)
        # handling cration of a new list item
        if request.data['itemName']:
            try:
                itemName = request.data['itemName']
                # retrieve useer from users table
                username = request.data['username']
                user = User.objects.get(username = username)
                # get the list istance for this list id
                list_obj = Lists.objects.get(user_id=user.id,listId = request.data['listId'])

                new_list_item = ListItems(
                    listId = list_obj,
                    itemName = itemName,
                    createdWhen = timezone.now(),
                    createdBy = user.id,
                    lastModified = timezone.now(),
                    lastModifiedBy = user.id,
                )
                
                new_list_item.save()
                

                return Response({
                    'id': str(new_list_item.id), 
                    "createdWhen": new_list_item.createdWhen
                    },status=200)
            
            except Exception as e:
                print(e)
                return Response({'error': str(e)}, status=500)
                    
    if request.method == 'PUT':
        try:
            update_type = request.data.get('updateType')
            print(update_type)
            username = request.data.get('username')
            user = User.objects.get(username=username)
            
            if update_type == 'title':
                list_id = request.data.get('listId')
                new_title = request.data.get('newListTitle')
                if new_title:
                    list_obj = Lists.objects.get(user_id=user.id, listId=list_id)
                    list_obj.listTitle = new_title
                    list_obj.lastModified = timezone.now()
                    list_obj.lastModifiedBy = user.id
                    list_obj.save()
                    return Response({'listTitle': new_title}, status=200)

            elif update_type == 'item':
                item_id = request.data.get('id')
                new_text = request.data.get('itemName')
                if item_id and new_text:
                    item = ListItems.objects.get(id=item_id)
                    item.itemName = new_text
                    item.lastModified = timezone.now()
                    item.lastModifiedBy = user.id
                    item.save()
                    return Response({'item': {'id': item_id, 'newText': new_text, 'lastModified': item.lastModified}}, status=200)
                
            elif update_type == 'toggleCheck':
                item_id = request.data.get('id')
                is_done = request.data.get('isDone')
                print(is_done)
                if item_id:
                    item = ListItems.objects.get(id=item_id)
                    item.isDone = is_done
                    item.lastModified = timezone.now()
                    item.lastModifiedBy = user.id
                    item.save()
                    return Response({'item': {'id': item_id, 'is_done': is_done, 'lastModified': item.lastModified}}, status=200)

            return Response({'error': 'Invalid update type or missing fields'}, status=400)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=500)
                        
    if request.method == 'DELETE':
        try:
            print(request)
            # Retrieve the user from the users table
            username = request.user
            user = User.objects.get(username=username)
            # get item id from request to know which item to delete
            id = request.GET.get('id')
            print('id',id)
            item_to_delete = ListItems.objects.get(id=id, createdBy=user.id)
            item_to_delete.delete()
            
            return Response({'message': f'deleted item with id {id}'})
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=500)