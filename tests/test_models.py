#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-hvad-cleanerversion
------------

Tests for `django-hvad-cleanerversion` models module.
"""

from datetime import datetime
import pytz

from django.test import TestCase
from django.utils.translation import activate

from hvad_cleanerversion import models
from tests.models import RegularModel, TranslatedModel, VersionedModel, TranslatedVersionedModel


class TestHvad_cleanerversion(TestCase):

    def setUp(self):
        activate('es')

    def test_from_regular(self):
        translated = TranslatedModel.objects.create(name="some")
        versioned = VersionedModel.objects.create(name="first")
        both = TranslatedVersionedModel.objects.create(name="first")
        regular = RegularModel.objects.create(
            translated=translated,
            versioned_regular=versioned,
            versioned=versioned,
            both=both,
        )

        t1 = datetime.utcnow().replace(tzinfo=pytz.utc)

        # check that a clean FK always uses the last relation

        versioned = versioned.clone()
        versioned.name = "second"
        versioned.save()

        both = both.clone_with_translations()
        both.name = "second"
        both.save()

        clean_regular = RegularModel.objects.get(pk=regular.pk)
        self.assertEqual(clean_regular.versioned_regular.name, "second")
        self.assertEqual(clean_regular.versioned.name, "second")

        self.assertEqual(clean_regular.get_versioned_relation('versioned', t1).name, "first")
        self.assertEqual(clean_regular.get_versioned_relation('both', t1).name, "first")

        # now try fallbacks
        translated = TranslatedVersionedModel.objects.get(id=both.id)
        translated = TranslatedVersionedModel.objects.language().fallbacks().get(pk=both.pk)

        activate('en')
        self.assertEqual(clean_regular.get_versioned_relation('versioned', t1).name, "first")
        self.assertEqual(clean_regular.get_versioned_relation('both', t1).name, "first")


    def tearDown(self):
        pass
