from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
from django.contrib.auth.models import User

class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    readers = models.ManyToManyField(User, related_name='permitted_tasks', through='TaskPermission', blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    expiration_date = models.DateTimeField(null=True)

    @property
    def expired(self):
        if self.expiration_date is not None and timezone.now() > self.expiration_date:
            return True
        return False

    @property
    def finishes_in_10_minutes(self):

        now = timezone.now()
        dt = self.expiration_date.replace(second=0, microsecond=0) - now.replace(second=0, microsecond=0)
        if dt == datetime.timedelta(minutes=10):
            return True
        return False
    

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class TaskPermission(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.BooleanField(default=False)
