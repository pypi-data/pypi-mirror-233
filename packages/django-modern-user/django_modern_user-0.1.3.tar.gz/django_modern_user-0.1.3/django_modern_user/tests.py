from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

ModernUser = get_user_model()


class ModernUserManagerTestCase(TestCase):
    def test_create_user_no_email(self):
        with self.assertRaises(ValueError) as context:
            ModernUser.objects._create_user(None, "password")
        self.assertTrue("Users must have an email address." in str(context.exception))

    def test_create_user_with_email(self):
        user = ModernUser.objects.create_user(
            email="john.doe@example.com", password="testpassword123"
        )
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_is_staff_false(self):
        with self.assertRaises(ValueError) as context:
            ModernUser.objects.create_superuser(
                email="john.doe@example.com", password="testpassword123", is_staff=False
            )
        self.assertTrue("Superuser must have is_staff=True." in str(context.exception))

    def test_create_superuser_is_superuser_false(self):
        with self.assertRaises(ValueError) as context:
            ModernUser.objects.create_superuser(
                email="john.doe@example.com",
                password="testpassword123",
                is_superuser=False,
            )
        self.assertTrue(
            "Superuser must have is_superuser=True." in str(context.exception)
        )

    def test_create_superuser(self):
        user = ModernUser.objects.create_superuser(
            email="john.doe@example.com", password="testpassword123"
        )
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class ModernUserTests(TestCase):
    def test_absence_of_default_fields(self):
        user = ModernUser.objects.create_user(
            email="test@example.com", password="testpassword123"
        )
        self.assertIsNone(user.username)
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.last_name)

    def test_lower_case_email(self):
        email = "Test@ExAMPle.com"
        user = ModernUser.objects.create_user(email=email, password="testpassword123")
        self.assertEqual(user.email, email.lower())

    def test_create_regular_user(self):
        user = ModernUser.objects.create_user(
            email="user@example.com", password="userpassword123"
        )
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = ModernUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword123"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_uniqueness(self):
        ModernUser.objects.create_user(
            email="unique@example.com", password="testpassword123"
        )
        with self.assertRaises(Exception):
            ModernUser.objects.create_user(
                email="unique@example.com", password="anotherpassword123"
            )
        # Testing case insensitivity
        with self.assertRaises(Exception):
            ModernUser.objects.create_user(
                email="UNIQUE@example.com", password="anotherpassword123"
            )

    def test_user_authentication(self):
        email = "auth@example.com"
        password = "testpassword123"
        ModernUser.objects.create_user(email=email, password=password)
        self.assertIsNotNone(authenticate(email=email, password=password))

    def test_required_fields(self):
        self.assertEqual(ModernUser.REQUIRED_FIELDS, [])

    def test_user_str(self):
        """Test the __str__ method of the ModernUser model."""
        user = ModernUser.objects.create_user(
            email="test@example.com", password="testpassword123"
        )
        self.assertEqual(user.__str__(), "test@example.com")
