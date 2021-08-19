from django.test import TestCase


def add(a, b):
  return a + b


class CalcTest(TestCase):

  def test_add(self):
    self.assertEqual(add(3, 8), 11)
