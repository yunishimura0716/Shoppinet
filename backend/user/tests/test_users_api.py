from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
  return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
  """Anyone who are not authorized can use public api"""

  def setUp(self):
    self.client = APIClient()

  def test_create_valid_user_success(self):
    """Test creating user with valid payload is successful"""
    payload = {
        'email': 'test@example.com',
        'password': 'testpassword',
        'name': 'Test name'
    }
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(**res.data)
    self.assertTrue(user.check_password(payload['password']))
    self.assertNotIn('password', res.data)

  def test_user_exists(self):
    """Test creating user that already exists"""
    payload = {
        'email': 'test@example.com',
        'password': 'testpassword',
        'name': 'Test name'
    }
    create_user(**payload)

    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_password_validation(self):
    """Test creating user with short password (must be more than 5)"""
    payload = {
        'email': 'test@example.com',
        'password': 'test',
        'name': 'Test name'
    }
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    user_exists = get_user_model().objects.filter(
        email=payload['email']
    ).exists()
    self.assertFalse(user_exists)

  def test_create_token_for_user(self):
    """Test creating token for new user"""
    payload = {'email': 'test@example.com', 'password': 'testpassword'}
    create_user(**payload)
    res = self.client.post(TOKEN_URL, payload)

    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_create_token_with_invalid_credential(self):
    """Test not creating token with invalid credential"""
    payload = {'email': 'test@example.com', 'password': 'testpassword'}
    create_user(**payload)
    payload['password'] = 'wrong'
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_no_user(self):
    """Test not creating toke for no user"""
    payload = {'email': 'test@example.com', 'password': 'testpassword'}
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_missing_fields(self):
    """Test not creating toke for missing fields"""
    payload = {'email': 'test@example.com', 'password': ''}
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
