from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import PortalUserCreationForm, PortalUserChangeForm
from .models import PortalUser

class PortalUserAdmin(UserAdmin):
    add_form = PortalUserCreationForm
    form = PortalUserChangeForm
    model = PortalUser
    list_display = ['email', 'username', 'battle_tag']

admin.site.register(PortalUser, PortalUserAdmin)