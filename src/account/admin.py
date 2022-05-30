from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Profile, City

User = get_user_model()


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    model = User
    list_display = ['username', 'email', 'email_verify']
    list_editable = ('email_verify',)
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'email_verify', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_preview', 'id')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True
