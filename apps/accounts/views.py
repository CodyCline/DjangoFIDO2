import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib.auth.hashers import check_password

from .models import Authenticator, CustomUser
from .forms import CustomUserCreationForm


from fido2.client import ClientData
from fido2.server import U2FFido2Server, RelyingParty, Fido2Server
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.ctap2 import AttestedCredentialData as att_data
from fido2.ctap1 import RegistrationData
from fido2.utils import sha256, websafe_encode, websafe_decode
from fido2 import cbor

rp = RelyingParty('localhost', 'Demo server')
server = Fido2Server(rp)


def user_create(request, template_name='accounts/signup.html'):
	form = CustomUserCreationForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('/')
	return render(request, template_name, {'form':form})


#These four views are for registering and verifying authenticators
@require_http_methods(['POST'])
def start_registration(request):
	#Creates a challenge with user_id and email and returns as CBOR data
	credentials = Authenticator.objects.get_credentials(user=request.user.username)

	registration_data, state = server.register_begin({
		'id': bytes(request.user.id),
		'name': request.user.email,
		'displayName': request.user.username
	}, credentials)

	request.session['state'] = state
	return HttpResponse(cbor.dumps(registration_data))

@require_http_methods(['POST'])
def end_registration(request):
	data = cbor.loads(request.body)[0]
	client_data = ClientData(data['clientDataJSON'])
	att_obj = AttestationObject(data['attestationObject'])
	auth_data = server.register_complete(
		request.session['state'],
		client_data,
		att_obj
	)
	
	encoded_auth = websafe_encode(auth_data.credential_data)
	new_key = Authenticator.objects.create_authenticator(
		login_id=request.user.id,
		auth_data = encoded_auth
	)
	
	del request.session['state'] 
	return HttpResponse("You're all set 🎉!")

@require_http_methods(['POST'])
def start_authentication(request):	
	#Parse the username as json
	body_unicode = request.body.decode('utf-8')
	data = json.loads(body_unicode)
	
	#Lookup current keys
	credentials = Authenticator.objects.get_credentials(user=data['username'])

	auth_data, state = server.authenticate_begin(credentials)
	request.session['state'] = state
	request.session['username'] = data['username']
	return HttpResponse(cbor.dumps(auth_data))

@require_http_methods(['POST'])
def finish_key(request):	
	data = cbor.loads(request.body)[0]
	credential_id = data['credentialId']
	client_data = ClientData(data['clientDataJSON'])
	auth_data = AuthenticatorData(data['authenticatorData'])
	signature = data['signature']	

	#Grab the credentials again from db use session to look up user
	
	credentials = Authenticator.objects.get_credentials(user=request.session['username'])
	
	server.authenticate_complete(
		request.session.pop('state'),
		credentials,
		credential_id,
		client_data,
		auth_data,
		signature
	)	

	user_logging_in = request.session['username'] # This needs to be session data
	password = CustomUser.methods.get_password_by_username(username=user_logging_in)
	user = CustomUser.objects.get(username=user_logging_in)	
	login(request, user)
	return HttpResponse('This checks out 👍')

#Views for editing or deleting keys. These will likely be ajax views
def edit_authenticator(request):
	return True

def delete_key(request):
	return True