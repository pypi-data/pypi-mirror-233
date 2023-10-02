from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ModernUser


@admin.register(ModernUser)
class ModernUserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field.

    You can find detailed examples here:
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#a-full-example
    https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username#Register%20your%20new%20User%20model%20with%20Django%20admin
    """

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "is_staff")
    search_fields = ("email",)
    ordering = ("email",)
