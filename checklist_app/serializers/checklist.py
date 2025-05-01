from rest_framework import serializers
from ..models import checklist

class ListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = checklist.Lists
        fields = ['listId','username','listTitle']

class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = checklist.ListItems
        fields = ['listId','itemName','notes','isDone']