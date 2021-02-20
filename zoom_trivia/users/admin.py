from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from zoom_trivia.users.forms import UserChangeForm, UserCreationForm
from zoom_trivia.users.models import GamePermissions

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + tuple(auth_admin.UserAdmin.fieldsets)
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(GamePermissions)
class GamePermissionAdmin(admin.ModelAdmin):
    list_display = ["pk", "game", "user", "role"]
