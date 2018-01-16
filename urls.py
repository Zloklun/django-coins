#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all/$', views.all_coins, name='all coins'),
    url(r'^all/json/$', views.all_coins_json, name='all_json'),
]
