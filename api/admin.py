from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'users_who_liked',)


admin.site.register(Post, PostAdmin)
