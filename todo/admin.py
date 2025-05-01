from django.contrib import admin
from .models import SharedList, Task

admin.site.register(SharedList)
admin.site.register(Task)