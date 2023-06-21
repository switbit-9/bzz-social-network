from datetime import datetime
from django.db import models


class Comment(models.Model):
        email = models.CharField(max_length=100)
        content = models.TextField(max_length=250)
        created = models.DateField(default=datetime.now())