from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class ModernUserManager(BaseUserManager):
    """A custum user manager that accounts for the modified fields of the custom User model.

    "Writing a manager for a custom user model" (Django docs):
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    """

    # Serialize the manager into migrations
    # https://docs.djangoproject.com/en/3.1/topics/migrations/#model-managers
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Perform the steps needed to create any kind of User."""
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Perform the unique steps needed to create a normal user."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Perform the unique steps needed to create a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class ModernUser(AbstractUser):
    """A custom user model for this project.

    Django highly recommends setting up a custom User model, even if the default user model is sufficient.
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    """

    # Remove some of the default fields.
    username = None
    first_name = None
    last_name = None

    # The email field should be required and unique (unlike default).
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"

    # Email is automatically required, since it is the USERNAME_FIELD.
    REQUIRED_FIELDS = []

    # Set the custom user manager
    objects = ModernUserManager()

    def save(self, *args, **kwargs):
        # Convert the email to lowercase before saving
        self.email = self.email.lower()
        super().save(*args, **kwargs)
