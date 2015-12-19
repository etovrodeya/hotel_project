from django.test import TestCase
from .models import Company

# Create your tests here.

class CompanyTest(TestCase):

    def test_str(self):
        company=Company(name='Газпром')
        self.assertEquals(
            str(company),
            'Газпром'
        )
