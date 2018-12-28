from __future__ import print_function, absolute_import, unicode_literals
import json
from django.shortcuts import render, redirect
from .models import User, Key
from fido2.client import ClientData
from fido2.server import U2FFido2Server, RelyingParty
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.ctap1 import RegistrationData
from fido2.utils import sha256, websafe_encode
from fido2 import cbor
from django.http.response import JsonResponse, HttpResponse


rp = RelyingParty('localhost', 'Demo FIDO2 server')
server = U2FFido2Server('http://localhost:8000', rp)

credentials = []


def index(request):
	return render(request, 'login/index.html')

def dashboard(request):
	return render(request, 'login/dashboard.html')

def register_user(request):
	attempt = User.objects.validate_user_creation(request.POST)
	if attempt:
		return redirect('index')
	else:
		return redirect('index')

def login_user(request):
	login_attempt = User.objects.validate_login(request.POST)
	if login_attempt:
		user = User.objects.get(email=request.POST['email'])
		request.session['login_credentials'] = {'id': user.id, 'email': user.email}
		return redirect('dashboard')

def register_key(request):
	return render(request, 'login/add.html')


#Key views
def begin_registration(request):
	login_creds = request.session['login_credentials'][0]
	print(login_creds)

	registration_data, state = server.register_begin({
		'id': bytes(login_creds['email']),
		'name': 'a_user',
	}, credentials)

	request.session['state'] = state
	return HttpResponse(cbor.dumps(registration_data))
		
	

def complete_registration(request):
	data = cbor.loads(request.body)[0]
	client_data = ClientData(data['clientDataJSON'])
	att_obj = AttestationObject(data['attestationObject'])
	auth_data = server.register_complete(
		request.session['state'],
		client_data,
		att_obj
	)

	credentials.append(auth_data.credential_data) #Write this to the db
	#Key.objects.validate_key_creation(request.POST) #Write to db
	return HttpResponse(cbor.dumps({'status': 'OK'}))

def test(request):
	message = "Test"
	return HttpResponse(message)