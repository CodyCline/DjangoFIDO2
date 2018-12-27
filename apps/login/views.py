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
server = U2FFido2Server('https://localhost:8000', rp)

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
		request.session['logged_in'] = User.objects.get(email=request.POST['email']).id
		return redirect('dashboard')

def register_key(request):
	return render(request, 'login/add.html')


#Key views
def begin_registration(request):
	# login_creds = request.session['logged_in']
	# print(login_creds('id'), login_creds('email'))
	
	registration_data, state = server.register_begin({
		'id': b'user_id',
		'name': 'a_user',
		'displayName': 'A. User',
		'icon': 'https://example.com/image.png'
	}, credentials)

	# session['state'] = state
	print(registration_data)
	print('\n\n\n\n')
	# cbor.loads(registration_data)
	try: 
		return cbor.dumps(registration_data)
	except AttributeError:
		return cbor.dumps(registration_data)
		
	

def complete_registration(request):
	data = cbor.loads(request.POST())
	print(data)
	client_data = ClientData(data['clientDataJSON'])
	att_obj = AttestationObject(data['attestationObject'])
	auth_data = server.register_complete(
		request.session['state'],
		client_data,
		att_obj
	)

	Key.objects.validate_key_creation(request.POST) #Write to db
	cbor.dumps({'status': 'OK'})
	# query = User.objects.
	#Write to db
	#auth_data.credential_data
def test(request):
	message = "Test"
	return HttpResponse(message)