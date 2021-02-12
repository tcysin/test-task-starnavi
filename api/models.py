from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_who_liked = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title