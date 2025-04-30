from rest_framework import serializers
from ..models import checklist

class ListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = checklist.Lists
        fields = ['list_id','user_id','list_title','list_type']

class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = checklist.ListItems
        fields = ['list_id','item_name','notes','is_done','due']