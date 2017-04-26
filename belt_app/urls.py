# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^users$',views.createUser),
	url(r'^login$',views.loginUser),
	url(r'^logout$',views.logout),
	url(r'^pokes$',views.pokes),
	url(r'^pokes/(?P<id>\d+)$',views.pokesAdd),
]


