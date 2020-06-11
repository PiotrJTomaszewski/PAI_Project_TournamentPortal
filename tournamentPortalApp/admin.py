from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import PortalUserCreationForm, PortalUserChangeForm
from .models import PortalUser


class PortalUserAdmin(UserAdmin):
    add_form = PortalUserCreationForm
    form = PortalUserChangeForm
    model = PortalUser
    list_display = ['email', 'first_name', 'last_name']
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_dummy')})
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(PortalUser, PortalUserAdmin)
