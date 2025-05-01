from django.db import models
from django.contrib.auth.models import User

class Lists(models.Model):
    listId = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    listTitle = models.CharField(max_length=30, default='New List')

class ListItems(models.Model):
    listId = models.ForeignKey(Lists, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=20)
    notes = models.CharField(default='',max_length=100)
    isDone = models.BooleanField(default=False)



    # LIST_TYPES = {
    #     '1': 'checklist',
    #     '2': 'to do',
    #     '3': 'groceries',
    #     '4': 'custom'
    # }
    # list_type = models.CharField(max_length=1, choices=LIST_TYPES, default='checklist')