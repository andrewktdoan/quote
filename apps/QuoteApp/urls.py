from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^quote$', views.quote),
    url(r'^user$', views.user),
    url(r'^logout$', views.logout),


]