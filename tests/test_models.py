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
from django.utils.timezone import now

from hvad_cleanerversion.models import get_versioned_relation, clone_with_translations, filter_versioned_relation
from tests.models import RegularModel, TranslatedModel, VersionedModel, TranslatedVersionedModel, RelatedModel


class TestHvad_cleanerversion(TestCase):

    def setUp(self):
        activate('es')


    def tearDown(self):
        pass

    def test_get_versioned_relation(self):
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

        both = clone_with_translations(both)
        both.name = "second"
        both.save()

        clean_regular = RegularModel.objects.get(pk=regular.pk)
        self.assertEqual(clean_regular.versioned_regular.name, "second")
        self.assertEqual(clean_regular.versioned.name, "second")

        self.assertEqual(get_versioned_relation(clean_regular, 'versioned', t1).name, "first")
        self.assertEqual(get_versioned_relation(clean_regular, 'both', t1).name, "first")

        # now try fallbacks
        translated = TranslatedVersionedModel.objects.get(id=both.id)
        translated = TranslatedVersionedModel.objects.language().fallbacks().get(pk=both.pk)

        activate('en')
        self.assertEqual(get_versioned_relation(clean_regular, 'versioned', t1).name, "first")
        self.assertEqual(get_versioned_relation(clean_regular, 'both', t1).name, "first")

    def test_get_versioned_related(self):
        origin = TranslatedVersionedModel.objects.create(name="first")
        regular = RegularModel.objects.create(
            both=origin,
        )
        RelatedModel.objects.create(origin=origin, name="first 1")
        RelatedModel.objects.create(origin=origin, name="first 2")

        t1 = datetime.utcnow().replace(tzinfo=pytz.utc)

        # manual cloning with relations
        timestamp = now()
        current = clone_with_translations(origin, timestamp)
        for related in current.related.as_of():
            clone_with_translations(related, timestamp)

        # modify the translated fields
        current.name = 'second'
        current.save()
        related = current.related.all()
        r1 = related[0]
        r1.name = "second 1"
        r1.save()
        r2 = related[1]
        r2.name = "second 2"
        r2.save()

        activate('en')
        clean_regular = RegularModel.objects.get(pk=regular.pk)
        versioned = get_versioned_relation(clean_regular, 'both', t1)
        self.assertEqual(versioned.name, 'first')
        filtered = filter_versioned_relation(versioned, 'related', t1)
        self.assertEqual(filtered[0].name, 'first 1')
        self.assertEqual(filtered[1].name, 'first 2')

        versioned = get_versioned_relation(clean_regular, 'both', None)
        self.assertEqual(versioned.name, 'second')
        filtered = filter_versioned_relation(versioned, 'related', None)
        self.assertEqual(filtered[0].name, 'second 1')
        self.assertEqual(filtered[1].name, 'second 2')
        
        # now check with another instance (that the filtering is working properly)
        another = TranslatedVersionedModel.objects.create(name="another")
        RelatedModel.objects.create(origin=another, name="another 1")
        RelatedModel.objects.create(origin=another, name="another 2")

        versioned = get_versioned_relation(clean_regular, 'both', None)
        self.assertEqual(versioned.name, 'second')
        filtered = filter_versioned_relation(versioned, 'related', None)
        self.assertEqual(filtered[0].name, 'second 1')
        self.assertEqual(filtered[1].name, 'second 2')
