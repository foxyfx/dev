from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'cv')}),
        ('Social media accounts', {'fields': ('facebook_username', 'facebook_password', 'instagram_username', 'instagram_password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'checkbox1', 'checkbox2')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    filter_horizontal = ('groups',)

admin.site.register(MyUser, MyUserAdmin)
