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
        User, through='Like', related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            # a user may like a given post only once
            models.UniqueConstraint(
                fields=('user', 'post'), name='unique_like')
        ]
    
    def __str__(self):
        return f'{self.user} likes {self.post}'