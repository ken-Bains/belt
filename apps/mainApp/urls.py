from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^new$', views.newUser),
    url(r'^signOn$', views.signOn),
    url(r'^success$', views.success),

]
