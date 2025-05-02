from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User 
from ..models.checklist import ListItems, Lists 
from django.utils import timezone

@api_view(['GET', 'POST', 'PUT'])
def checklist(request):
    if request.method == 'POST':
        if request.data['listItem']:
            try:
                list_item = request.data['listItem']
                # get the list istance for this list id
                list = Lists.objects.get(listId = request.data['listId'])
                # retrieve useer from users table
                username = request.data['username']
                user = User.objects.get(username = username)

                new_list_item = ListItems(
                    listId = list.listId,
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
        print(request.data)
        try:
            # get the list istance for this list id
            list = Lists.objects.get(listId = request.data['listId'])
            # get all the list items in this list
            items = ListItems.objects.filter(listId = request.data['listId'])
            print(items)
            return Response(status=200)
        except Exception as e:
            print(e)
            return Response(e)