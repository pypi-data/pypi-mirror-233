from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Comment(models.Model):
    """
    Core comment model that utilizes the Django Content Type
    framework to implement a decoupled/non-model Comments system
    """
    content = models.TextField()
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content} ..."

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
