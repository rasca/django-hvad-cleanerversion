# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from hvad_cleanerversion.urls import urlpatterns as hvad_cleanerversion_urls

urlpatterns = [
    url(r'^', include(hvad_cleanerversion_urls, namespace='hvad_cleanerversion')),
]
