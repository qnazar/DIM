from django.contrib import admin

from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_teacher', 'is_staff')
    list_filter = ('is_teacher', 'is_staff')
    search_fields = ('first_name', 'last_name', 'username')


admin.site.register(MyUser, MyUserAdmin)
