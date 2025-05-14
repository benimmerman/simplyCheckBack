from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Lists(models.Model):
    listId = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    listTitle = models.CharField(max_length=100, default="")
    createdWhen = models.DateTimeField(default=timezone.now)
    lastModified = models.DateTimeField(null=True)
    lastModifiedBy = models.IntegerField(null=True)

class ListItems(models.Model):
    listId = models.ForeignKey(Lists, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=1000)
    notes = models.CharField(null=True,max_length=4000)
    isDone = models.BooleanField(default=False)
    createdWhen = models.DateTimeField(default=timezone.now)
    createdBy = models.IntegerField(default=1)
    lastModified = models.DateTimeField(null=True)
    lastModifiedBy = models.IntegerField(null=True)



    # LIST_TYPES = {
    #     '1': 'checklist',
    #     '2': 'to do',
    #     '3': 'groceries',
    #     '4': 'custom'
    # }
    # list_type = models.CharField(max_length=1, choices=LIST_TYPES, default='checklist')