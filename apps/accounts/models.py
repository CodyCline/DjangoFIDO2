from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class ModelManager(models.Manager):
    def post_valid(self, form_data, ):
        if len(post_data['text'] > 2):
            self.create(
                author = 1,
                text = 'the text',
            )

class CustomUser(AbstractUser):
    # add additional fields in here
    phone_num = models.CharField(max_length=30)

    # def __str__(self):
    #     return self.email