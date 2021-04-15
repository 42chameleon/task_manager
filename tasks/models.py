from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_tasks'
    )
    name = models.CharField(max_length=1024)
    description = models.TextField()
    date_end = models.DateTimeField()
    file = models.FileField(upload_to='tasks/files/', blank=True)

    def __str__(self):
        return self.name
