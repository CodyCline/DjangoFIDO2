import datetime
from django.contrib.auth.models import AbstractUser, UserManager
from fido2.ctap2 import AttestedCredentialData as att_data
from django.db import models
from django.conf import settings
from fido2 import cbor

class ModelManager(models.Manager): 
	#This may end up being a queryset
	def create_authenticator(self, login_id, auth_data):
		user_id = CustomUser.objects.get(id=login_id)
		new_authenticator = self.create(
			user = user_id,
			name="Newly Registered Device",
			encoded_data=auth_data,
			created_at=datetime.date,
			last_used=datetime.date
		)
		new_authenticator.save()
		return new_authenticator.id
	
	def add_auth_data(self, key_id, auth_data, user):
		authenticator_id = Authenticator.objects.get(id = key_id)
		user_id = CustomUser.objects.get(id = user)
		self.create(
			authenticator=authenticator_id,
			user=user_id,
			aaguid = auth_data.aaguid,
			credential_id = auth_data.credential_id,
			public_key = cbor.dump_dict(auth_data.public_key)		
		)

	def get_credentials(self, user):
		query_list = []
		user_id = CustomUser.objects.get(username=user).id
		#TODO return statement if username not found
		auth_query = Authenticator.objects.filter(user=user_id).all()

		#Also need to use exists() method
		#Grab each AttestedCredentialData that belongs to an Authenticator
		# whose user_id matches up with the logged in user' id
		#This is where we will probably need to reconstruct the data
		#to be in a proper format
		for i in auth_query:
			att_query = AttestedCredentialData.objects.get(authenticator=i)
			query_list.append(att_query)

		return query_list
	
	def get_password_by_username(self, username):
		the_user = CustomUser.objects.get(username=user).password
		return the_user


class CustomUser(AbstractUser):
	# Extends built-in user
	phone_num = models.CharField(max_length=12)
	objects = UserManager()
	methods = ModelManager()

#Contains meta-data on a registered device
#TODO add number of time(s) used
class Authenticator(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="keys", on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	encoded_data = models.CharField(max_length=950)
	last_used = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	objects = ModelManager()

#The actual cryptographic data stored from the device for verification
class AttestedCredentialData(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="attObj", on_delete=models.CASCADE)
	authenticator = models.OneToOneField(
		Authenticator,
		on_delete=models.CASCADE
	)

	aaguid = models.BinaryField()
	credential_id = models.BinaryField()
	public_key = models.BinaryField()
	objects = ModelManager()

