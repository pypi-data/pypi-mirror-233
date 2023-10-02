# Django Modern User

Django Modern User is a custom user model for Django projects that replaces the default `username` field with a case-insensitive `email` field for authentication, and removes the requirement for first and last names. This model aims to provide a more practical and modern approach to user management in Django.

## Installation

1. Install `django-modern-user` via pip:
   ```bash
   python -m pip install django-modern-user
   ```

2. Add `django_modern_user` to your `INSTALLED_APPS` in your Django settings:
   ```python
   INSTALLED_APPS = [
       # ... other apps
       'django_modern_user',
   ]
   ```

3. Set `django_modern_user.ModernUser` as your user model:
   ```python
   AUTH_USER_MODEL = "django_modern_user.ModernUser"
   ```

4. Run migrations to create the necessary database table:
   ```bash
   python manage.py migrate
   ```

## Usage

With `django-modern-user`, authentication is done using the email field. The email field is case-insensitive, ensuring a user-friendly authentication process.

Here's an example of how you might create a new user:

```python
from django_modern_user.models import ModernUser

# Create a new user
user = ModernUser.objects.create_user(email='example@example.com', password='password123')

# Create a superuser
superuser = ModernUser.objects.create_superuser(email='admin@example.com', password='password123')
```

## Custom User Manager

`django-modern-user` comes with a custom user manager, `UserPlusManager`, which handles user creation and ensures the email field is used for authentication.

## Further Customization

You can further customize the `ModernUser` model and `UserPlusManager` to meet the specific needs of your project.

## Contributing

Feel free to fork the project, open a PR, or submit an issue if you find bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
