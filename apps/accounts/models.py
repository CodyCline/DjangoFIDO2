import datetime

from django.shortcuts import HttpResponse
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings

from fido2.ctap2 import AttestedCredentialData
from fido2.utils import websafe_encode, websafe_decode

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
	
	def get_credentials(self, user):
		#Function finds all authenticator's registered to user and returns 
		# it as a list 
		query_list = []
		username = CustomUser.objects.get(username=user).id
		auth_query = Authenticator.objects.filter(user=username).all()
		for cred in auth_query.iterator():
			query = cred.encoded_data
			decode = AttestedCredentialData(websafe_decode(query))
			query_list.append(decode)
		return query_list

	#This will update the 'last_used' property every 
	# time a user logs in or registers a new device
	def update_authenticator(self, key):
		return True


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
	encoded_data = models.CharField(max_length=950) #Data stored from key
	last_used = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	objects = ModelManager()

