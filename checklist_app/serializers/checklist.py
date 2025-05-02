from rest_framework import serializers
from ..models import checklist

class ListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = checklist.Lists
        fields = '__all__'

class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = checklist.ListItems
        fields = '__all__'