import datetime
from django.shortcuts import HttpResponse
from django.contrib.auth.models import AbstractUser, UserManager
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
	
	def get_credentials(self, user):
		#This needs to grab the credentials that belong to a user based on username
		query_list = []
		user_id = CustomUser.objects.get(username=user).id
		#TODO return statement if username not found
		if user_id.exists() is None:
			return HttpResponse("We can't find that user")
		#Also need to use exists() method to check if they have any keys
		auth_query = Authenticator.objects.filter(user=user_id).all()
		if auth_query.exists():
			for i in auth_query:
				query_list.append(Authenticator.objects.only('encoded_data').get(user=user_id).encoded_data)
			return query_list
		else:
			return HttpResponse('Not found')
		
		#Grab each AttestedCredentialData that belongs to an Authenticator
		# whose user_id matches up with the logged in user' id
		#This is where we will probably need to reconstruct the data
		#to be in a proper format
		return query_list
	
	def get_password_by_username(self, username):
		the_user = CustomUser.objects.get(username=user).password
		return the_user

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
	encoded_data = models.CharField(max_length=950)
	last_used = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	objects = ModelManager()

