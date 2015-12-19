from django.test import TestCase
from .models import Room, Service

# Create your tests here.

class RoomTest(TestCase):

    def test_str(self):
        room=Room(housing=4,floor=2,number=1)
        self.assertEquals(
            str(room),
            '421',
        )

class ServiceTest(TestCase):

    def test_str(self):
        service=Service(name='Билет на концерт')
        self.assertEquals(
            str(service),
            'Билет на концерт',
        )
