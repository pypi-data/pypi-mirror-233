from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Comment(models.Model):
    """
    Core comment model that utilizes the Django Content Type
    framework to implement a decouple/non-model tied
    Comments system
    """
    object_id = models.PositiveIntegerField()
    content = models.CharField(max_length=255)
    content_object = GenericForeignKey("content_type", "object_id")
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content[:10]}... on {self.content_type.model}"

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
