import json, ast
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import Http404
from .forms import CustomUserCreationForm, AuthenticatorCreationForm
from .models import Authenticator
from fido2.client import ClientData
from fido2.server import U2FFido2Server, RelyingParty
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.ctap1 import RegistrationData
from fido2.utils import sha256, websafe_encode
from fido2 import cbor
from ast import literal_eval

rp = RelyingParty('localhost', 'Demo FIDO2 server')
server = U2FFido2Server('https://localhost:8080', rp)

credentials = [] #For now store the credentials in memory


def user_create(request, template_name='accounts/signup.html'):
	form = CustomUserCreationForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('/')
	return render(request, template_name, {'form':form})


#These four views are fetched from the front end for registering verifying authentication
@require_http_methods(['POST'])
def start_registration(request):
	user_id = request.user.id
	user_email = request.user.email
	#Creates a challenge with user_id and email and returns as CBOR data
	registration_data, state = server.register_begin({
		'id': bytes(user_id),
		'name': user_email,
		'displayName': 'New Key'
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

	#Write the key to the database
	# Authenticator.objects.validate_key_creation(
	# 	auth_data=auth_data.credential_data,
	# 	login_id=request.user.id
	# )

	print(type(auth_data), '\n\n\n', auth_data)

	credentials.append(auth_data.credential_data) #For now for testing purposes

	del request.session['state'] #Pop the session data
	return HttpResponse(cbor.dumps({'status': 'OK'}))

@require_http_methods(['POST'])
def start_authentication(request):

	return HttpResponse("OK")

@require_http_methods(['POST'])
def finish_key(request):
	
	data = cbor.loads(request.body)[0]
	credential_id = data['credentialId']
	client_data = ClientData(data['clientDataJSON'])
	auth_data = AuthenticatorData(data['authenticatorData'])
	signature = data['signature']

	server.authenticate_complete(
		request.session.pop('state'),
		credentials,
		credential_id,
		client_data,
		auth_data,
		signature
	)
	return HttpResponse(cbor.dumps({'status': 'OK'}))

#Views for editing or deleting keys. These will likely be ajax endpoints
def edit_authenticator(request):
	return True

def delete_key(request):
	return True