import json
from django.shortcuts import render, redirect
from .models import User

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
	return render(request, 'login/addkey.html')

def second_factor_auth(request):
	return True

