from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Achievement, UserFollowing
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "is_staff",
                    "is_active", "is_superuser", "date_joined"]
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active", "is_superuser", "date_joined"),
        }),
    )
    search_fields = ("email", "username")
    ordering = ("email",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_achievements', 'location', 'birth_date')

    def display_achievements(self, obj):
        return ", ".join([achievement.title for achievement in obj.achievements.all()])
    display_achievements.short_description = 'Achievements'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserFollowing)
admin.site.register(Achievement)
