from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin, GroupAdmin
from django.contrib.auth.models import Group as AuthGroup

from .models import User, Group


class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mobile')}),
        (_('Status'), {'fields': ('is_active', 'is_verified', 'is_registered')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Extra'), {'classes': ('collapse', 'close'), 'fields': ('pin', 'last_generated')}),
    )

    list_display = (
        'username',
        'email',
        'mobile',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'is_verified',
        'is_registered',
        'pin')
    search_fields = AuthUserAdmin.search_fields + ('mobile',)
    list_filter = AuthUserAdmin.list_filter + ('is_verified', 'is_registered')
    readonly_fields = ('pin', 'date_joined', 'last_login', 'is_registered',
                       'is_verified', 'last_generated')


admin.site.register(User, UserAdmin)
admin.site.unregister(AuthGroup)
admin.site.register(Group, GroupAdmin)
