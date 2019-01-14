from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import Http404
from .models import Authenticator, AttestedCredentialData
from .forms import CustomUserCreationForm
from fido2.client import ClientData
from fido2.server import U2FFido2Server, RelyingParty
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.ctap1 import RegistrationData
from fido2.utils import sha256, websafe_encode
from fido2 import cbor

rp = RelyingParty('localhost', 'Demo FIDO2 server')
server = U2FFido2Server('https://localhost:9000', rp)

credentials = [] #For now store the credentials in memory


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

	#Write the authenticator (meta data about the key) and the actual cryptographic data to db
	new_key = Authenticator.objects.create_authenticator(
		login_id=request.user.id
	)


	AttestedCredentialData.objects.add_auth_data(
		key_id=new_key,
		auth_data = auth_data.credential_data
	)


	credentials.append(auth_data.credential_data) #For now for testing purposes
	del request.session['state'] #Pop the session data
	return HttpResponse(cbor.dumps({'status': 'OK'}))

@require_http_methods(['POST'])
def start_authentication(request):
	
	credentials = "Credentials that are owned by the user grabbed from db"

    auth_data, state = server.authenticate_begin(credentials)
    session['state'] = state
    return HttpResponse(cbor.dumps(auth_data))

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