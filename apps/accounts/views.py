from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomUserCreationForm
from .models import CustomUser

def user_create(request, template_name='accounts/signup.html'):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, template_name, {'form':form})
