from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='accounts/home.html'), name='home'),
    path('add/', TemplateView.as_view(template_name='accounts/add_key.html'), name='home'),
    path('auth/', TemplateView.as_view(template_name='accounts/authenticate.html'), name='home'),
    path('accounts/signup/', views.user_create, name='signup'),
    #Register and authenticate key routes
    path('register/begin', views.start_registration, name='begin_registration'),
    path('register/complete', views.end_registration, name='complete_registration'),
    path('auth/begin', views.start_authentication, name='start_auth'),
    path('auth/complete', views.finish_key, name='finish_auth')
    
]


