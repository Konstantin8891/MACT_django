from django.db import models


class Museum(models.Model):
    service = models.URLField()
    link = models.URLField()
    title = models.TextField()
    content = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
