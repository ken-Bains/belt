from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^new$', views.newUser),
    url(r'^signOn$', views.signOn),
    url(r'^books$', views.all_books),
    url(r'^logout$', views.logout),
    url(r'^book/add$', views.book_add_page),
    url(r'^book/(?P<id>\d)+$$', views.one_book),
    url(r'^add_new_book$', views.add_new_book),
    url(r'^user/(?P<id>\d)+$', views.user_info_page),
    url(r'^add_review$', views.add_review),
]
