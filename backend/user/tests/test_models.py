from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

  def test_create_user_with_email_successful(self):
    """Create user with email successful"""
    email = "test@example.com"
    password = "testPassword09"
    user = get_user_model().objects.create_user(
        email=email,
        password=password
    )

    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))

  def test_new_user_email_normalized(self):
    """Create user with normalized email"""
    email = "test@EXAMPLE.com"
    user = get_user_model().objects.create_user(email, 'testpassword')

    self.assertEqual(user.email, email.lower())

  def test_email_validation(self):
    """create user with valdiated email"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(None, 'testpassword')

  def test_create_new_superuser(self):
    """Create new super user"""
    user = get_user_model().objects.create_superuser('test@example.com', 'testpassword')

    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)
