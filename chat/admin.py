from django.contrib import admin

# Register your models here.

from .models import User, AppToken

admin.site.register(User)
admin.site.register(AppToken)
