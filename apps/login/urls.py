from django.conf.urls import url
from . import views
urlpatterns = [
    #Key URLS
    url(r'^register/begin$', views.begin_registration, name='begin_key'),
    url(r'^register/complete$', views.complete_registration, name='end_key'),
]