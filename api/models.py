from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    # we delete all author posts when he vanishes
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title