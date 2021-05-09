from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Rating
import random

User = get_user_model() #user.objects.all()



class RatingTestCase(TestCase):

    def create_users(self, user_num):
        item = []
        for i in range(0, self.user_num):
            item.append(User(username = f'user_{i}'))
        User.objects.bulk_create(item)


    def setUp(self):
        user_num = random.randint(10, 100)
        self.create_users(user_num)