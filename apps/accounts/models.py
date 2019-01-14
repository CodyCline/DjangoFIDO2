import datetime
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings
from fido2 import cbor

class ModelManager(models.Manager): 
	#This may end up being a queryset
	def create_authenticator(self, login_id):
		user_id = CustomUser.objects.get(id=login_id)
		new_authenticator = self.create(
			user = user_id,
			name="Newly Registered Device",
			created_at=datetime.date,
			last_used=datetime.date
		)
		new_authenticator.save()
		return new_authenticator.id
	
	def add_auth_data(self, key_id, auth_data):
		authenticator_id = Authenticator.objects.get(id = key_id)
		self.create(
			authenticator=authenticator_id,
			aaguid = auth_data.aaguid,
			credential_id = auth_data.credential_id,
			public_key = cbor.dump_dict(auth_data.public_key)
		)

	def get_credentials(self, login_id):
		query_list = []
		user_id = CustomUser.objects.get(id=login_id)
		auth_query = Authenticator.objects.filter(user=user_id).all()

		#Grab each AttestedCredentialData that belongs to an Authenticator
		# whose id's match the logged in user's id
		for i in auth_query:
			query_list.append(AttestedCredentialData.objects.get(authenticator=i))
		print(query_list)
		return query_list


class CustomUser(AbstractUser):
	# Extends built-in user
	phone_num = models.CharField(max_length=12)
	objects = UserManager()

#Contains meta-data on a registered device
class Authenticator(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="keys", on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	last_used = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	objects = ModelManager()

class AttestedCredentialData(models.Model):
	authenticator = models.OneToOneField(
		Authenticator,
		on_delete=models.CASCADE
	)
	aaguid = models.BinaryField()
	credential_id = models.BinaryField()
	public_key = models.BinaryField()
	objects = ModelManager()