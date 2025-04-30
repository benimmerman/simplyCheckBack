from django.db import models
from django.contrib.auth.models import User

class Lists(models.Model):
    listId = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listTitle = models.CharField(max_length=30, default='New List')

class ListItems(models.Model):
    listId = models.ForeignKey(Lists, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=20)
    # notes = models.CharField(max_length=40)
    # is_done = models.BooleanField()
    # due = models.DateField()





    # Create your models here
# class Users(models.Model):
#     SUBSCRIPTIONS = {
#         'P': 'premium',
#         'S': 'standard'
#     }
#     user_id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=50)
#     # username = models.CharField(max_length=15)
#     # password = models.CharField(max_length=30)
#     subscription = models.CharField(max_length=1, choices=SUBSCRIPTIONS, default='standard')




    # LIST_TYPES = {
    #     '1': 'checklist',
    #     '2': 'to do',
    #     '3': 'groceries',
    #     '4': 'custom'
    # }
    # list_type = models.CharField(max_length=1, choices=LIST_TYPES, default='checklist')