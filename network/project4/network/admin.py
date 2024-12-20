from django.contrib import admin
from .models import Post,User,Follow,Like



admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)

# Register your models here.
