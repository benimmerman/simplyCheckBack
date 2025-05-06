from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User 
from ..models.checklist import ListItems, Lists 
from django.utils import timezone

@api_view(['GET', 'POST', 'PUT'])
def checklist(request, username=None, list_id=None):
    print(request.method)
    if request.method == 'PUT':
        # handling new title
        if request.data['newListTitle']:
            try:
                # retrieve useer from users table
                username = request.data['username']
                user = User.objects.get(username = username)
                # get the list istance for this list id
                list_obj = Lists.objects.get(listId = request.data['listId'])
                # new title from request
                new_list_title = request.data['newListTitle']
                # update the title and save
                list_obj.listTitle = new_list_title
                list_obj.save()

                return Response({'listTitle': new_list_title}, status=200)
            
            except Exception as e:
                print(e)
                return Response({'error': str(e)}, status=500)
        
    if request.method == 'POST':
        
        # handling cration of a new list item
        if request.data['listItem']:
            try:
                list_item = request.data['listItem']
                # retrieve useer from users table
                username = request.data['username']
                user = User.objects.get(username = username)
                # get the list istance for this list id
                list_obj = Lists.objects.get(user_id=user.id,listId = request.data['listId'])
                

                new_list_item = ListItems(
                    listId = list_obj.listId,
                    itemName = list_item,
                    createdWhen = timezone.now,
                    createdBy = user.id,
                    lastModified = timezone.now,
                    lastModifiedBy = user.id,
                )
                
                new_list_item.save()

                return Response({'listItemId': new_list_item.id})
            
            except Exception as e:
                print(e)
                return Response({'error': str(e)}, status=500)
    
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
            item_data = list(items.values('id', 'itemName', 'isDone', 'notes'))
            print(item_data)
            return Response({'listItems': item_data},status=200)
        except Exception as e:
            print(e)
            return Response(e)