from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

  def setUp(self):
    self.client = Client()
    self.admin_user = get_user_model().objects.create_superuser(
        email='admin@example.com',
        password='adminpassword'
    )
    self.client.force_login(self.admin_user)
    self.user = get_user_model().objects.create_user(
        email='test@example.com',
        password='testpassword',
        name='Test user full name'
    )

  def test_users_listed(self):
    """Test that users are listed on user page"""
    url = reverse('admin:user_user_changelist')
    res = self.client.get(url)

    self.assertContains(res, self.user.name)
    self.assertContains(res, self.user.email)

  def test_users_edit(self):
    """Test that user edit page works"""
    url = reverse('admin:user_user_change', args=[self.user.id])
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)

  def test_users_add(self):
    """Test taht suer add page works"""
    url = reverse('admin:user_user_add')
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)
