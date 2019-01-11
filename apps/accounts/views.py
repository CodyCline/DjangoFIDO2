from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, HttpResponse
from fido2.client import ClientData
from fido2.server import U2FFido2Server, RelyingParty
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.ctap1 import RegistrationData
from fido2.utils import sha256, websafe_encode
from fido2 import cbor
from .forms import CustomUserCreationForm
from .models import CustomUser


rp = RelyingParty('localhost', 'Demo FIDO2 server')
server = U2FFido2Server('https://localhost:8000', rp)

credentials = []

def user_create(request, template_name='accounts/signup.html'):
	form = CustomUserCreationForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('/')
	return render(request, template_name, {'form':form})


#These four views are fetched from the front end for registering verifying authentication
def start_registration(request):
	user_id = request.user.id
	user_email = request.user.email
	registration_data, state = server.register_begin({
		'id': bytes(user_id),
		'name': user_email,
		'displayName': 'New Key'
	}, credentials)

	request.session['state'] = state
	return HttpResponse(cbor.dumps(registration_data))

def end_registration(request):
	user_id = request.user.id
	data = cbor.loads(request.body)[0]
	client_data = ClientData(data['clientDataJSON'])
	att_obj = AttestationObject(data['attestationObject'])
	auth_data = server.register_complete(
		request.session['state'],
		client_data,
		att_obj
	)

	credentials.append(auth_data.credential_data) #Write this to the db
	
	del request.session['state'] #Pop the session data
	return HttpResponse(cbor.dumps({'status': 'OK'}))

def start_authentication(request):
	return True

def finish_key(request):
	return True

#Renaming a key
def edit_authenticator(request):
	return True

#Deleting a key
def delete_key(request):
	return True