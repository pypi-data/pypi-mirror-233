#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from geonames import api

urlpatterns = [
    path('countries/', api.countries, name='countries'),
    path('municipalities/', api.municipalities, name='municipalities'),
]