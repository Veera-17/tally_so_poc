from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# Extend the UserAdmin to display full name & email
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
