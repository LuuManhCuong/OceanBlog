from django.contrib import admin
from .models import User, Blog, Asset, Comment


# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Asset)
admin.site.register(Comment)
