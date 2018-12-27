from django.db import models
from datetime import datetime



class ManageModels(models.Manager):
	# def __init__(self):
	#     return True
	def validate_login(self, post_data):
		#if len(self.filter(email=post_data.get('email'))) > 0:
			#given_password = post_data.get('password')
			#correct_password = User.objects.get(email = post_data.get('email').password #Email associated with the password
			#if post_data.get('password') == post_data.get('email').password:
				#print("Password Correct")
		return True

	
	def validate_user_creation(self, post_data):
		self.create (
			username=post_data.get('username'),
			email=post_data.get('email'),
			password=post_data.get('password'),
			two_factor_authenticated=False,
			created_at=datetime.now(),
			updated_at=datetime.now()
		)
		return True

	def validate_key_creation(self, request):
		login_credentials = request.session['logged_in'].id
		User.objects.filter(id=login_credentials).update(
			two_factor_authenticated = True
		)

		self.create(
			user = login_credentials,
			credential_data_key = request.get('auth_data.credential_data')

		)
		return True

	def validate_key_login(self):
		return True

class User(models.Model):
	username = models.TextField(max_length=100)
	two_factor_authenticated = models.BooleanField(null=False) 
	email = models.TextField(max_length=100) 
	password = models.TextField(max_length=200) 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ManageModels()

class Key(models.Model):
	user = models.ForeignKey(User, related_name="keys", on_delete=models.CASCADE)
	key_name = models.TextField(max_length="100")
	credential_data_key = models.TextField(unique=True) #Public key
	key_handle = models.TextField()
	app_id = models.TextField()
	objects = ManageModels()
