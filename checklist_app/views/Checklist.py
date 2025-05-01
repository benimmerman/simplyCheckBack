from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.checklist import ListItems, Lists 

@api_view(['GET', 'POST', 'PUT'])
def checklist(request):
    if request.method == 'POST':
        print(request)
        print('inside checklist post api')
        return Response({'message': 'successful connection to checklist post api'})