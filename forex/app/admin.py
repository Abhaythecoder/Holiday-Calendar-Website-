from django.contrib import admin
from .models import APIkey, Login

# Register your models here.

admin.site.register(APIkey)


class LoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']


admin.site.register(Login, LoginAdmin)
