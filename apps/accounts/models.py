import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class ModelManager(models.Manager): 
	#This may end up being a queryset
	def validate_key_creation(self, auth_data, login_id):
		user_id = CustomUser.objects.get(id=login_id)
		self.create(
			user = user_id,
			name="Newly Registered Device",
			key_hash = auth_data,
			created_at=datetime.date,
			last_used=datetime.date
		)
		return True
	def get_credential_id(self, login_id):
		user_id = CustomUser.objects.get(id=login_id)
		return Authenticator.objects.only('key_hash').get(user=user_id).key_hash


class CustomUser(AbstractUser):
	# Extends built-in user
	phone_num = models.CharField(max_length=12)
	objects = ModelManager()

#Contains meta-data on a registered device
class Authenticator(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="keys", on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	last_used = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)

class AttestedCredentialData(models.Model):
	authenticator = models.ForeignKey(
		Authenticator,
		on_delete=models.CASCADE,
	)
	aaguid = models.BinaryField()
	_credential_id = models.BinaryField(db_column='credential_id')
	_public_key = models.BinaryField(db_column='public_key')