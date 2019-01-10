from __future__ import print_function, absolute_import, unicode_literals
import json
from django.shortcuts import render, redirect
# from .models import User, Key
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
	id_credential = request.session['login_user_id']
	user_id = User.objects.get(id=id_credential)
	context = {
		'all_keys': Key.objects.get(user=user_id)
		# 'all_keys': Key.objects.all()
	}
	return render(request, 'login/dashboard.html', context)


def register_key(request):
	return render(request, 'login/add.html')


#Key views
def begin_registration(request):
	id_credential = request.session['login_user_id']
	email_credential = request.session['login_user_email']
	# print(login_creds, 'The users credentials')
	# bytes(ofobject)
	registration_data, state = server.register_begin({
		'id': bytes(id_credential),
		'name': email_credential,
		'displayName': 'users key name'
	}, credentials)

	request.session['state'] = state
	return HttpResponse(cbor.dumps(registration_data))
		
	

def complete_registration(request):
	id_credential = request.session['login_user_id']
	data = cbor.loads(request.body)[0]
	client_data = ClientData(data['clientDataJSON'])
	att_obj = AttestationObject(data['attestationObject'])
	auth_data = server.register_complete(
		request.session['state'],
		client_data,
		att_obj
	)

	credentials.append(auth_data.credential_data) #Write this to the db
	del request.session['state']
	Key.objects.validate_key_creation(request, public_key=auth_data.credential_data) #Write to db
	return HttpResponse(cbor.dumps({'status': 'OK'}))
