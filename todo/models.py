from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SharedList(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

PRIORITY_CHOICES = [
    ('L', 'Low'),
    ('M', 'Medium'),
    ('H', 'High'),
]

class Task(models.Model):
    shared_list = models.ForeignKey(SharedList, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    finish_by = models.DateField(null=True, blank=True)  # Optional deadline

    def __str__(self):
        return self.title
