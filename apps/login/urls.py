from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^register$', views.register_user, name='register_user'),
    url(r'^login$', views.login_user, name='login_user'),
    url(r'^keyregister$', views.register_key, name='key_register'),
    #Key URLS
    url(r'^register/begin$', views.begin_registration, name='begin_key'),
    url(r'^register/complete$', views.complete_registration, name='end_key'),
]