from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('accounts/signup/', views.user_create, name='signup'),
    path('', TemplateView.as_view(template_name='accounts/home.html'), name='home'),
]


