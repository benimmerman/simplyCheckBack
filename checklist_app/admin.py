from django.contrib import admin
from .models import checklist

admin.site.register(checklist.ListItems)
admin.site.register(checklist.Lists)