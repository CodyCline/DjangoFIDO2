from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime



# class ManageModels(models.Manager):
# 	def validate_login(self, post_data):
# 		attempt = True
# 		errors = []
# 		if len(User.objects.filter(email=post_data['email'])) > 0:
# 			hashed_pw = User.objects.get(email = post_data['email']).password
# 			hashed = hashed.encode('utf-8')
# 			password = post_data['password']
# 			if bcrypt.hashpw(password, hashed) == hashed_pw:
# 				attempt = True
# 			else:
# 				errors.append("Unsuccessful login.")
# 				attempt = False
# 		else:
# 			errors.append("Unsuccessful login.")
# 			attempt = False
# 		return [attempt, errors]

	
# 	def validate_user_creation(self, post_data):
# 		passFlag = True
# 		errors = []
# 		#VALIDATE FORMAT
# 		if len(post_data['name']) < 3:
# 			errors.append('Name must be at least 3 characters.')
# 			passFlag = False            
# 		if not re.match(NAME_REGEX, post_data['name']):
# 			errors.append('Name fields must be letter characters only.')
# 			passFlag= False
# 		if not re.match(EMAIL_REGEX, post_data['email']):
# 			errors.append("Invalid email format.")
# 			passFlag = False
# 		if len(post_data['password']) < 8:
# 			errors.append('Password must contain at least 8 characters.')
# 			passFlag = False
# 		if post_data['password'] != post_data['confirm_password']:
# 			errors.append('Passwords do not match.')
# 			passFlag = False
# 		if len(self.filter(email=post_data['email'])) > 0:
# 			errors.append("Registration is invalid.")
# 			passFlag = False

# 		if passFlag == True:
# 			hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())
# 			self.create(
# 				username = post_data['username'], 
# 				email = post_data['email'], 
# 				password = hashed
# 			)
# 		return [passFlag, errors]

	
	
	
# 	def validate_key_creation(self, request, public_key):
# 		login_credentials = request.session['login_user_id']
# 		the_user = User.objects.get(id=login_credentials)
# 		self.create(
# 			user = the_user,
# 			credential_data_key = public_key
# 		)
# 		return True

# 	def validate_key_login(self):
# 		return True

# class User(models.Model):
# 	username = models.TextField(max_length=100)
# 	two_factor_authenticated = models.BooleanField(null=False) 
# 	email = models.TextField(max_length=100) 
# 	password = models.TextField(max_length=200) 
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
# 	objects = ManageModels()

# class Key(models.Model):
# 	user = models.ForeignKey(User, related_name="keys", on_delete=models.CASCADE)
# 	key_name = models.TextField(max_length="100")
# 	credential_data_key = models.TextField(unique=True) #Public key
# 	key_handle = models.TextField()
# 	app_id = models.TextField()
# 	objects = ManageModels()
